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

    # Calculate text size
    text_width, text_height = draw.textsize(text, font=font)
    
    # Calculate position for bottom-center alignment
    width, height = image.size
    x = (width - text_width) // 2
    y = height - text_height - 10  # Offset from bottom, adjust as needed

    # Calculate background size and position
    bg_width = text_width + 20  # Add padding
    bg_height = text_height + 20  # Add padding
    bg_x = (width - bg_width) // 2
    bg_y = height - text_height - 30  # Adjust vertical position as needed

    # Draw background rectangle
    draw.rectangle([(bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height)], fill='black')

    # Draw text on the image
    draw.text((x, y), text, font=font, fill='white')
    
    return image

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text('Hi! Send me a photo and I will add text to it.')
    logger.info("Start command received")

@app.on_message(filters.photo)
async def handle_photo(client, message: Message):
    try:
        logger.info("Photo message received")
        photo = await message.download()  # Download the highest quality photo
        logger.info(f"Photo downloaded to {photo}")
        
        image = Image.open(photo)
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
