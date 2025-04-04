from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import io
import numpy as np
from collections import Counter

app = Flask(__name__, static_folder='static')
CORS(app)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    try:
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        image = image.resize((100, 100))
        pixels = np.array(image).reshape(-1, 3)
        pixels = [tuple(p) for p in pixels]
        color_counts = Counter(pixels)
    except Exception as e:
        return jsonify({"error": "Image processing failed", "details": str(e)}), 500

    def rgb_to_hex(rgb): return '#{:02x}{:02x}{:02x}'.format(*rgb)

    colors = [
        {
            "rgb": f"rgb{c}",
            "hex": rgb_to_hex(c),
            "count": count
        }
        for c, count in color_counts.items()
    ]

    return jsonify({"colors": colors})


if __name__ == '__main__':
    app.run(debug=True)
