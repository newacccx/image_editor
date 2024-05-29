import io
import logging
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your API ID, API Hash, and Bot Token
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ensure that all necessary environment variables are set
if not all([API_ID, API_HASH, BOT_TOKEN]):
    logger.error("One or more environment variables are missing: API_ID, API_HASH, BOT_TOKEN")
    raise EnvironmentError("One or more environment variables are missing")

# Convert API_ID to integer
API_ID = int(API_ID)

# Create a new Client instance
app = Client("image_text_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def add_text_to_image(image: Image.Image, text: str) -> Image.Image:
    draw = ImageDraw.Draw(image)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_size = 52
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        logger.error(f"Font file not found: {font_path}")
        raise

    width, height = image.size
    
    # Calculate text size using textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    
    # Calculate position for bottom-center alignment
    x = (width - text_width) // 2
    y = height - text_height - 10  # Offset from bottom, adjust as needed

    # Draw a black rectangle as background for text
    padding = 10
    text_background = Image.new('RGBA', (text_width + 2 * padding, text_height + 2 * padding), (0, 0, 0, 200))
    image.paste(text_background, (x - padding, y - padding), text_background)
    
    # Draw text on the image
    draw.text((x, y), text, font=font, fill='white')
    
    return image

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text('Hi! Send me a photo or a photo link and I will add text to it.')
    logger.info("Start command received")

@app.on_message(filters.photo)
async def handle_photo(client, message: Message):
    try:
        logger.info("Photo message received")
        processing_message = await message.reply_text("Processing...")
        photo = await message.download()  # Download the highest quality photo
        logger.info(f"Photo downloaded to {photo}")
        
        image = Image.open(photo)
        text = "Telegram-@HDCINEMA_1"

        modified_image = add_text_to_image(image, text)
        bio = io.BytesIO()
        bio.name = 'image.png'
        modified_image.save(bio, 'PNG')
        bio.seek(0)

        await client.send_photo(chat_id=message.chat.id, photo=bio)
        await processing_message.delete()
        logger.info("Photo sent back to user")
    except Exception as e:
        logger.error(f"Error handling photo: {e}")
        await message.reply_text('An error occurred while processing your photo.')

@app.on_message(filters.text & filters.regex(r'^https?://'))
async def handle_photo_link(client, message: Message):
    try:
        logger.info("Photo link received")
        processing_message = await message.reply_text("Processing...")
        response = requests.get(message.text)
        image = Image.open(BytesIO(response.content))
        text = "Telegram-@HDCINEMA_1"

        modified_image = add_text_to_image(image, text)
        bio = io.BytesIO()
        bio.name = 'image.png'
        modified_image.save(bio, 'PNG')
        bio.seek(0)

        await client.send_photo(chat_id=message.chat.id, photo=bio)
        await processing_message.delete()
        logger.info("Photo sent back to user")
    except Exception as e:
        logger.error(f"Error handling photo link: {e}")
        await message.reply_text('An error occurred while processing the photo link.')

if __name__ == "__main__":
    app.run()
