from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import io
import tensorflow as tf

app = Flask(__name__)

model_path = "m1.h5"
model = tf.keras.models.load_model(model_path)

def preprocess_image(image):
    # Add your preprocessing steps, like resizing, scaling, etc.
    # This example assumes the model expects a 224x224 image
    img = image.resize((256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = tf.expand_dims(img_array, 0)
    return img_array

def predict(image):
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)
    predicted_class = "Normal" if prediction[0][0] > 0.5 else "Abnormal"
    return predicted_class

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
