import base64
import os

def load_icon(filename):
    filepath = os.path.join("app/assets/icons", filename)
    with open(filepath, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded}"
