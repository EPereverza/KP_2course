### Имитация аномалии «Потерянное обновление» на примере управления запасами книг в библиотеке
Что такое аномалия «Потерянное обновление»? </br>
Аномалия "потерянное обновление" возникает, когда две транзакции одновременно читают одни и те же данные, изменяют их и записывают обратно, перезаписывая изменения друг друга.
</br>
Теоретические способы предотвращения с лекции:
- Использование более строгих уровней изоляции (SERIALIZABLE)
- Явная блокировка строк с помощью SELECT FOR UPDATE
- Оптимистичные блокировки (проверка версии записи перед обновлением)

Ход работы:

- Создание и начальное заполнение таблиц books и book_loans
- Аномалия. </br>
    Функция loan_book выдаёт книгу читателю. При уровне изоляции READ COMMITTED два параллельных запроса могут прочитать одинаковое количество книг, и оба решат, что книга есть в наличии. В результате происходит "потерянное обновление" - количество книг уменьшается только на 1, хотя выдано 2 экземпляра. 
- Способы предотвращения. </br>
    - Установить уровень изоляции SERIALIZABLE. Данный уровеньгарантирует, что параллельные транзакции будут выполняться так, как если бы они выполнялись последовательно. 
    - Явная блокировка строк (SELECT FOR UPDATE). Блокирует строку для других транзакций до завершения текущей

Код :
```python
import psycopg2
import threading
import time
from datetime import datetime
from dotenv import load_dotenv
import os
from tabulate import tabulate

# Загрузка переменных окружения
load_dotenv()

# Параметры подключения к PostgreSQL
DB_PARAMS = {
    'host': 'localhost',
    'port': 5432,
    'database': 'KP16',
    'user': 'postgres',
    'password': os.getenv('PGPASSWORD')
}

def setup_db():
    """Создание таблиц базы данных для библиотеки"""
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            # Таблица книг
            cur.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    quantity INTEGER CHECK (quantity >= 0) NOT NULL
                );
            """)
            # Таблица выдачи книг
            cur.execute("""
                CREATE TABLE IF NOT EXISTS book_loans (
                    id SERIAL PRIMARY KEY,
                    book_id INTEGER REFERENCES books(id),
                    client_name TEXT NOT NULL,
                    loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    return_date TIMESTAMP
                );
            """)
            conn.commit()
    print("Database setup complete.")

def seed_initial_books():
    """Заполнение базы начальными данными о книгах"""
    books = [
        ("Война и мир", "Лев Толстой", 5),
        ("Преступление и наказание", "Фёдор Достоевский", 3),
        ("1984", "Джордж Оруэлл", 7),
        ("Мастер и Маргарита", "Михаил Булгаков", 4)
    ]
    
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM book_loans;")
            cur.execute("DELETE FROM books;")
            cur.execute("ALTER SEQUENCE books_id_seq RESTART WITH 1;")
            cur.execute("ALTER SEQUENCE book_loans_id_seq RESTART WITH 1;")
            
            for title, author, quantity in books:
                cur.execute(
                    "INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)",
                    (title, author, quantity)
                )
            conn.commit()
    print("Initial books seeded.")

def print_tables():
    """Печать содержимого таблиц"""
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            print("\nBooks:")
            cur.execute("SELECT * FROM books;")
            print(tabulate(cur.fetchall(), headers=[desc[0] for desc in cur.description]))
            
            print("\nBook Loans:")
            cur.execute("SELECT * FROM book_loans;")
            print(tabulate(cur.fetchall(), headers=[desc[0] for desc in cur.description]))

def loan_book(book_id, client_name, isolation_level="READ COMMITTED"):
    """
    Функция выдачи книги читателю.
    Демонстрирует проблему потерянного обновления при низком уровне изоляции.
    """
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        conn.set_session(isolation_level=isolation_level, autocommit=False)
        
        with conn.cursor() as cur:
            # Начало транзакции
            cur.execute("BEGIN;")
            
            # Проверка наличия книги
            cur.execute("SELECT quantity FROM books WHERE id = %s;", (book_id,))
            result = cur.fetchone()
            
            if not result:
                raise Exception(f"Книга с ID {book_id} не найдена")
                
            quantity = result[0]
            
            # Искусственная задержка для демонстрации проблемы
            time.sleep(2)
            
            # Если книга есть в наличии, уменьшаем количество и создаем запись о выдаче
            if quantity > 0:
                cur.execute(
                    "UPDATE books SET quantity = quantity - 1 WHERE id = %s;", 
                    (book_id,)
                )
                cur.execute(
                    "INSERT INTO book_loans (book_id, client_name) VALUES (%s, %s);",
                    (book_id, client_name)
                )
                conn.commit()
                print(f"[{datetime.now()}] {client_name} получил книгу ID {book_id}")
            else:
                conn.rollback()
                print(f"[{datetime.now()}] Книга ID {book_id} отсутствует на складе")
                
    except Exception as e:
        conn.rollback()
        print(f"[{datetime.now()}] Ошибка при выдаче книги: {e}")
    finally:
        conn.close()

def simulate_lost_update():
    """Моделирование ситуации потерянного обновления"""
    print("\n=== Моделирование потерянного обновления ===")
    print("Два библиотекаря одновременно выдают последний экземпляр книги")
    
    # Выбираем книгу с небольшим количеством экземпляров
    book_id = 2  # Преступление и наказание (изначально 3 экземпляра)
    
    # Создаем два потока, имитирующих двух библиотекарей
    librarian1 = threading.Thread(
        target=loan_book, 
        args=(book_id, "Читатель Иванов", "READ COMMITTED")
    )
    librarian2 = threading.Thread(
        target=loan_book, 
        args=(book_id, "Читатель Петров", "READ COMMITTED")
    )
    
    librarian1.start()
    librarian2.start()
    
    librarian1.join()
    librarian2.join()
    
    print("\nИтоговое состояние:")
    print_tables()

def prevent_lost_update():
    """Демонстрация способов предотвращения потерянного обновления"""
    print("\n=== Способы предотвращения потерянного обновления ===")
    
    # Восстанавливаем исходные данные
    seed_initial_books()
    
    # Использование SERIALIZABLE уровня изоляции
    print("\n1. Использование SERIALIZABLE уровня изоляции:")
    
    book_id = 2
    librarian1 = threading.Thread(
        target=loan_book, 
        args=(book_id, "Читатель Сидоров", "SERIALIZABLE")
    )
    librarian2 = threading.Thread(
        target=loan_book, 
        args=(book_id, "Читатель Кузнецов", "SERIALIZABLE")
    )
    
    librarian1.start()
    librarian2.start()
    
    librarian1.join()
    librarian2.join()
    
    print_tables()
    
    # Использование SELECT FOR UPDATE (блокировка строк)
    print("\n2. Использование SELECT FOR UPDATE (блокировка строк):")
    
    seed_initial_books()
    
    def loan_book_with_lock(book_id, client_name):
        """Версия функции с явной блокировкой строки"""
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            conn.set_session(autocommit=False)
            
            with conn.cursor() as cur:
                cur.execute("BEGIN;")
                
                # Блокируем строку для обновления
                cur.execute(
                    "SELECT quantity FROM books WHERE id = %s FOR UPDATE;", 
                    (book_id,)
                )
                result = cur.fetchone()
                
                if not result:
                    raise Exception(f"Книга с ID {book_id} не найдена")
                    
                quantity = result[0]
                
                time.sleep(2)  # Искусственная задержка
                
                if quantity > 0:
                    cur.execute(
                        "UPDATE books SET quantity = quantity - 1 WHERE id = %s;", 
                        (book_id,)
                    )
                    cur.execute(
                        "INSERT INTO book_loans (book_id, client_name) VALUES (%s, %s);",
                        (book_id, client_name)
                    )
                    conn.commit()
                    print(f"[{datetime.now()}] {client_name} получил книгу ID {book_id}")
                else:
                    conn.rollback()
                    print(f"[{datetime.now()}] Книга ID {book_id} отсутствует на складе")
                    
        except Exception as e:
            conn.rollback()
            print(f"[{datetime.now()}] Ошибка при выдаче книги: {e}")
        finally:
            conn.close()
    
    book_id = 2
    librarian1 = threading.Thread(
        target=loan_book_with_lock, 
        args=(book_id, "Читатель Николаев")
    )
    librarian2 = threading.Thread(
        target=loan_book_with_lock, 
        args=(book_id, "Читатель Михайлов")
    )
    
    librarian1.start()
    librarian2.start()
    
    librarian1.join()
    librarian2.join()
    
    print_tables()

if __name__ == "__main__":

    setup_db()
    seed_initial_books()
    

    print("\nНачальное состояние:")
    print_tables()
    
    # проблема
    simulate_lost_update()
    
    # решение
    prevent_lost_update()
```