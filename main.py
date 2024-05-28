import io
import logging
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your API ID, API Hash, and Bot Token
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ensure that all necessary environment variables are set
if not all([API_ID, API_HASH, BOT_TOKEN]):
    logger.error("One or more environment variables are missing: API_ID, API_HASH, BOT_TOKEN")
    raise EnvironmentError("One or more environment variables are missing")

# Create a new Client instance
app = Client("image_text_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def add_text_to_image(image: Image.Image, text: str) -> Image.Image:
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    width, height = image.size
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, font=font, fill='white')
    return image

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text('Hi! Send me a photo and I will add text to it.')
    logger.info("Start command received")

@app.on_message(filters.photo)
async def handle_photo(client, message: Message):
    try:
        logger.info("Photo message received")
        photo = message.photo[-1]
        photo_file = await client.download_media(photo)
        logger.info(f"Photo downloaded to {photo_file}")
        
        image = Image.open(photo_file)
        text = "Sample Text"

        modified_image = add_text_to_image(image, text)
        bio = io.BytesIO()
        bio.name = 'image.png'
        modified_image.save(bio, 'PNG')
        bio.seek(0)

        await message.reply_photo(photo=bio)
        logger.info("Photo sent back to user")
    except Exception as e:
        logger.error(f"Error handling photo: {e}")
        await message.reply_text('An error occurred while processing your photo.')

if __name__ == "__main__":
    app.run()
