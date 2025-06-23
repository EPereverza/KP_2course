from flask import Flask, request, jsonify, render_template_string
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

app = Flask(__name__)

# Генерация RSA ключей (публичный и приватный)
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Шифрование
def rsa_encrypt(text, public_key):
    encrypted = public_key.encrypt(
        text.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

# Расшифровка
def rsa_decrypt(encrypted_text, private_key):
    decrypted = private_key.decrypt(
        encrypted_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

# Генерация ключей
private_key, public_key = generate_rsa_keys()

# HTML
@app.route('/')
def index():
    html_form = """
    <html>
        <body>
            <h2>Шифрование и расшифровка с RSA</h2>
            
            <!-- Форма для шифрования -->
            <form action="/encrypt" method="post">
                <h3>Введите текст для шифрования:</h3>
                <textarea name="text_to_encrypt" rows="1" cols="50"></textarea><br><br>
                <input type="submit" value="Зашифровать">
            </form>

            <!-- Форма для расшифровки -->
            <form action="/decypher" method="post">
                <h3>Введите зашифрованный текст для расшифровки (в base64):</h3>
                <textarea name="text_to_decrypt" rows="1" cols="50"></textarea><br><br>
                <input type="submit" value="Расшифровать">
            </form>
        </body>
    </html>
    """
    return render_template_string(html_form)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    text = request.form.get('text_to_encrypt')
    if not text:
        return jsonify({"error": "Введите текст для шифрования!"}), 400

    # Шифруем
    encrypted_data = rsa_encrypt(text, public_key)

    # Возвращаем данные в base64
    return jsonify({"encrypted_data": encrypted_data.hex()})

# Маршрут для расшифровки
@app.route('/decypher', methods=['POST'])
def decypher():
    encrypted_data_hex = request.form.get('text_to_decrypt')
    if not encrypted_data_hex:
        return jsonify({"error": "Введите зашифрованный текст для расшифровки!"}), 400

    encrypted_data = bytes.fromhex(encrypted_data_hex)

    # Расшифровываем
    decrypted_data = rsa_decrypt(encrypted_data, private_key)

    return jsonify({"decrypted_data": decrypted_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
