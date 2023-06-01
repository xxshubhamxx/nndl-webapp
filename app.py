from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import io

app = Flask(__name__)

def predict(image):
    # TODO: Load your model and predict the class
    return "Normal"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            image = Image.open(file.stream)
            predicted_class = predict(image)
            return render_template('result.html', prediction=predicted_class)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)