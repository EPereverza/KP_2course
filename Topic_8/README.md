## LR6_КП_4semester
```
Напишите корневой адрес работающего по https веб-приложения 
(+ ссылку на борд/репозиторий с кодом решения), которое по маршруту /size2json 
получает по имени поля image в формате multipart/form-data изображение в формате PNG и 
выдаёт JSON-строку вида {"width":123,"height":456}, содержащую, соответственно, 
ширину и высоту изображения в пикселях.

По маршруту /login приложение должно выдавать ваш логин в этой системе (MOODLE).

Требования: 

Все данные возвращаются в json, заголовки ответов должны быть соответствующие данным.
Формат ответа по маршруту /login {"author": "__ваш логин__"}
Если передана не картинка, возвращать json: {"result":"invalid filetype"}
Усложнения (дают: вероятность повышение итоговой оценки за модуль, прирост кармы и т.д.): 

Реализация дополнительных решений более чем с 1 фреймворком (Варианты: Node.js, Django, Go)
Реализация фронтэнда и отправка данных на сервер с использованием какого-либо фронтэнд-фреймворка.
Реализация асинхронной отправки данных, получение результата без перезагрузки страницы по отдельному маршруту, сохранение "состояния" (приложение помнит какой последний файл загружался и выводит данные по нему).
Вывод и отображение самого изображения на страницу с формой или другую страницу как thumbnail.
```

```python
from flask import Flask, request, jsonify, render_template_string
from PIL import Image

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Upload Image</title>
    <script>
        function previewImage(event) {
            var reader = new FileReader();
            reader.onload = function(){
                var output = document.getElementById('thumbnail');
                output.src = reader.result;
                output.style.display = 'block';
            }
            reader.readAsDataURL(event.target.files[0]);
        }
    </script>
</head>
<body>
    <h2>Загрузите png картинку</h2>
    <form action="/size2json" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/png" required onchange="previewImage(event)">
        <button type="submit">Посмотреть размеры</button>
    </form>
    <br>
    <img id="thumbnail" src="#" alt="Image preview" style="display:none; max-width: 200px; max-height: 200px; border: 1px solid #ddd;">
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/size2json', methods=['POST'])
def size2json():
    if 'image' not in request.files:
        return jsonify({"error": "no file provided"}), 400

    file = request.files['image']

    if file.filename == '' or not file.filename.lower().endswith('.png'):
        return jsonify({"error": "invalid filetype"}), 400

    try:
        image = Image.open(file)
        width, height = image.size
        return jsonify({"width": width, "height": height})
    except Exception:
        return jsonify({"error": "error processing image"}), 500

@app.route('/login')
def login():
    return jsonify(1149912)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

```