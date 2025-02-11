"""API endpoint for generating quote images"""

import io
import imgkit

from PIL import Image

from fastapi.responses import Response

from app import api, config
from app.quotes.models import Messages
from app.quotes.generate import generate_messages


@api.post("/generate", tags=["Generation"])
async def quote_generate(form: Messages):
    """Generates a WEBP image from the provided quote message data"""

    result = imgkit.from_string(
        string=generate_messages(form),
        output_path=None,
        options={
            "format": "png",
            "transparent": "",
            "enable-local-file-access": "",
            "quiet": "",
            "width": 1792
        },
        css=config.defaults.templates_path / "styles.css"
    )

    original_image = Image.open(io.BytesIO(result))
    cropped_image = original_image.crop(original_image.getbbox())

    webp_output = io.BytesIO()
    cropped_image.save(webp_output, format="WEBP", optimize=True, quality=config.settings.quote.quality)
    webp_output.seek(io.SEEK_SET)

    return Response(content=webp_output.getvalue(), media_type="image/webp")
