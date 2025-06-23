from flask import Flask, request, jsonify, render_template_string, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Upload Image</title>
</head>
<body>
    <h2>Сгенерировать картинку</h2>
    <form action="/makeimage" method="get">
        <label>Width: <input type="number" name="width" required></label><br>
        <label>Height: <input type="number" name="height" required></label><br>
        <label>Text: <input type="text" name="text" required></label><br>
        <button type="submit">Создать картинку</button>
    </form>
    <h3>Результат:</h3>
    <img src="data:image/jpg;base64,{{ image_data }}">
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

@app.route('/makeimage', methods=['GET'])
def makeimage():
    try:
        width = int(request.args.get('width', ''))
        height = int(request.args.get('height', ''))
        text = request.args.get('text', '')
    except ValueError:
        return render_template_string(HTML_FORM, message="Invalid image size")

    if width <= 0 or height <= 0 or width > 2000 or height > 2000:
        return render_template_string(HTML_FORM, message="Invalid image size")


    image = Image.new("RGB", (width, height), (255,255,255))
    draw = ImageDraw.Draw(image)

    draw.text((10,10), text, fill='black')

    image.save("test.jpg")

    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)

    base64_image = base64.b64encode(img_io.read()).decode('utf-8')
    encoded_img = f"{base64_image}"

    return render_template_string(HTML_FORM, image_data=encoded_img)

@app.route('/login')
def login():
    return jsonify({"author": "1149912"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
