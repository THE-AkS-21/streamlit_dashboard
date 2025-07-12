import base64
import os

def load_icon(icon_name: str) -> str:
    icon_path = os.path.join("app/assets/icons", icon_name)
    with open(icon_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/svg+xml;base64,{encoded}"
