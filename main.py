from flask import Flask, request, jsonify
from PIL import Image, UnidentifiedImageError
import io
from collections import Counter

app = Flask(__name__)


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string."""
    return "#{:02x}{:02x}{:02x}".format(*rgb)


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    try:
        image = Image.open(io.BytesIO(file.read()))
        image = image.convert('RGB')
    except UnidentifiedImageError:
        return jsonify({"error": "Invalid image file"}), 400

    # Resize for faster processing while keeping aspect ratio
    image.thumbnail((100, 100))

    # Extract pixel data
    pixels = list(image.getdata())

    # Count most common colors
    color_counts = Counter(pixels)
    top_colors = color_counts.most_common(5)

    # Convert RGB tuples to hex
    top_colors = [
        {"rgb": f"rgb({color[0][0]}, {color[0][1]}, {color[0][2]})",
         "hex": rgb_to_hex(color[0])}
        for color in top_colors
    ]

    return jsonify({"colors": top_colors})


if __name__ == '__main__':
    app.run(debug=True)
