import os
import tensorflow as tf
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
from io import BytesIO

app = Flask(__name__)

# --- Load Model ---
MODEL_PATH = 'waste_classifier_model.h5'
model = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
DUSTBIN_MAP = {
    'cardboard': '🔵 Blue Dustbin (Dry Waste / Recyclable)',
    'glass': '🔵 Blue Dustbin (Dry Waste / Recyclable)',
    'metal': '🔵 Blue Dustbin (Dry Waste / Recyclable)',
    'paper': '🔵 Blue Dustbin (Dry Waste / Recyclable)',
    'plastic': '🔵 Blue Dustbin (Dry Waste / Recyclable)',
    'trash': '⚫ Black Dustbin (General / Non-Recyclable Waste)'
}

def preprocess_image(image_bytes):
    """Prepares the image for the model."""
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return preprocessed_img

@app.route('/predict', methods=['POST'])
def predict():
    """Handles prediction requests."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    try:
        file = request.files['image']
        image_bytes = file.read()
        processed_image = preprocess_image(image_bytes)

        prediction = model.predict(processed_image)
        score = tf.nn.softmax(prediction[0])
        predicted_class = CLASS_NAMES[np.argmax(score)]
        confidence = float(np.max(score))

        return jsonify({
            'predicted_class': predicted_class,
            'confidence': f"{confidence:.2%}",
            'recommended_dustbin': DUSTBIN_MAP.get(predicted_class)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Railway provides the PORT environment variable
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)