### Тема 15
### Задание
Сделайте копию борда. https://colab.research.google.com/drive/1l_d-c7r2IQxyFVdG_ZOp739hC3ub6NgD#scrollTo=7-zp0KZLWg_p

Откройте доступ к борду, укажите в самой первой текстовой ячейке свое ФИО.

Заполните пропущенные ячейки с кодом, в которых написан комментарий # TODO. 

Выполнить скрапинг со страницы новостей РГПУ им. А. И. Герцена и создайте файл csv на основе данных, а также, при необходимости - тексты самих новостей с именами в формате айди_новости.txt.


Пример кода для применения модели к новому тексту:

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

### Загружаем обученную модель и векторизатор (если они были сохранены)
model = joblib.load('logreg_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

### Новый текст для анализа
new_texts = [
    "Очень плохой сервис, я разочарован",
    "Это лучший день в моей жизни!",
    "Нейтральное сообщение без выраженной эмоции"
]

### Преобразуем текст в векторы
X_new = vectorizer.transform(new_texts)

### Предсказываем тональность
predictions = model.predict(X_new)

### Если у тебя модель возвращает бинарные классы: 0 - негатив, 1 - позитив
for text, pred in zip(new_texts, predictions):
    sentiment = "позитивная" if pred == 1 else "негативная"
    print(f"Текст: {text}\n→ Тональность: {sentiment}\n")
Как сохранить и загрузить модель и векторизатор

import joblib

joblib.dump(trained_model, 'logreg_model.pkl')
joblib.dump(tfidf_vectorizer, 'vectorizer.pkl')

### Результат:
`https://colab.research.google.com/drive/1ctKS91br01d4dBhl52dFI4l6_Mr0fIET?usp=sharing`