from flask import Flask, render_template, request, make_response
import qrcode
import io
import base64

app = Flask(__name__)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code_img = None
    if request.method == 'POST':
        data = request.form.get('qr_data')
        if data:
            qr_code_img = generate_qr_code(data)
        else:
            return "Please provide data to generate the QR code."
    return render_template('index.html', qr_code_img=qr_code_img)

if __name__ == '__main__':
    app.run(debug=True)
