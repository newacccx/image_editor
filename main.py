import io
import logging
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
API_ID = '6381607'
API_HASH = '9799ad1623afe9bad664501f984b71fe'
BOT_TOKEN = '6153579279:AAEyzLHm9p8L8t0M7kn40TnhGYOlu3jI3jY'

# Create a new Client instance
app = Client("image_text_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def add_text_to_image(image: Image.Image, text: str) -> Image.Image:
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    width, height = image.size
    text_width, text_height = draw.textsize(text, font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, font=font, fill='white')
    return image

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text('Hi! Send me a photo and I will add text to it.')

@app.on_message(filters.photo)
async def handle_photo(client, message: Message):
    photo = message.photo
    photo_file = await client.download_media(photo)
    image = Image.open(photo_file)
    text = "Sample Text"

    modified_image = add_text_to_image(image, text)
    bio = io.BytesIO()
    bio.name = 'image.png'
    modified_image.save(bio, 'PNG')
    bio.seek(0)

    await message.reply_photo(photo=bio)

if __name__ == "__main__":
    app.run()
