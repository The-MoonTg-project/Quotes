"""API endpoint for generating quote images"""

import io
import math

import plutoprint
from PIL import Image

from fastapi.responses import Response

from app import api, config
from app.quotes.models import Messages
from app.quotes.generate import generate_messages


@api.post("/generate", tags=["Generation"])
async def quote_generate(form: Messages):
    """Generates a WEBP image from the provided quote message data"""

    css_path = config.defaults.templates_path / "styles.css"
    user_style = css_path.read_text(encoding="utf-8")

    book = plutoprint.Book(media=plutoprint.MEDIA_TYPE_SCREEN)
    book.load_html(generate_messages(form), user_style=user_style)

    width = min(math.ceil(book.get_document_width()), 1792)
    height = math.ceil(book.get_document_height())

    png_buffer = io.BytesIO()
    book.write_to_png_stream(png_buffer, width=width, height=height)
    png_buffer.seek(0)

    original_image = Image.open(png_buffer)
    cropped_image = original_image.crop(original_image.getbbox())

    webp_output = io.BytesIO()
    cropped_image.save(webp_output, format="WEBP", optimize=True, quality=config.settings.quote.quality)
    webp_output.seek(io.SEEK_SET)

    return Response(content=webp_output.getvalue(), media_type="image/webp")
