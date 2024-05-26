from flask import Flask, request, render_template, redirect
from PIL import Image
import easyocr
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Read the image file in memory
            image_bytes = file.read()
            image = Image.open(BytesIO(image_bytes))

            # Perform OCR on the image
            text = extract_text_from_image(image)

            # Encode image to base64
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            return render_template('index.html', text=text, image_data=img_str)
    return render_template('index.html', text=None, image_data=None)

def extract_text_from_image(image):
    # Convert PIL image to a numpy array
    image_np = np.array(image)

    # Perform OCR
    text = reader.readtext(image_np, detail=0)  # detail=0 to get only the text
    return ' '.join(text)

if __name__ == '__main__':
    app.run(debug=True)
