import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image, ImageDraw, ImageFont
import io

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your Telegram Bot Token
TOKEN = '6153579279:AAEyzLHm9p8L8t0M7kn40TnhGYOlu3jI3jY'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a photo and I will add text to it.')

def add_text_to_image(image: Image.Image, text: str) -> Image.Image:
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    width, height = image.size
    text_width, text_height = draw.textsize(text, font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, font=font, fill='white')
    return image

def handle_photo(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_bytes = photo_file.download_as_bytearray()
    image = Image.open(io.BytesIO(photo_bytes))
    text = "Sample Text"

    modified_image = add_text_to_image(image, text)
    bio = io.BytesIO()
    bio.name = 'image.png'
    modified_image.save(bio, 'PNG')
    bio.seek(0)

    update.message.reply_photo(photo=bio)

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
