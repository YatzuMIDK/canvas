from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from PIL import Image
import requests
from io import BytesIO

app = FastAPI()

@app.get("/gay")
async def overlay_image(image_url: str, opacity: float = 0.5):
    try:
        # Obtener la imagen principal desde la URL proporcionada
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        # Cargar la imagen que se va a sobreponer
        overlay_url = "https://i.ibb.co/996YQBr/Putos.jpg"
        overlay_response = requests.get(overlay_url)
        overlay_response.raise_for_status()
        overlay = Image.open(BytesIO(overlay_response.content)).convert("RGBA")

        # Redimensionar la imagen overlay para que tenga el mismo tamaño que la imagen principal
        overlay = overlay.resize(image.size)

        # Aplicar la opacidad
        overlay = overlay.copy()
        alpha = overlay.split()[3]
        alpha = alpha.point(lambda p: p * opacity)
        overlay.putalpha(alpha)

        # Superponer la imagen overlay sobre la imagen principal
        image = image.convert("RGBA")
        combined = Image.alpha_composite(image, overlay)

        # Guardar la imagen resultante en un buffer
        buffer = BytesIO()
        combined.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
