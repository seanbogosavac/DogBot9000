import logging
import os
from logging.handlers import RotatingFileHandler
from PIL import Image, UnidentifiedImageError

from .bot_instance import bot
from .loops import daily_pistouche


# Configure logging
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "log.txt")

handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3)
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# Optional HEIC support
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    logger.warning("pillow-heif not installed, HEIC images won't be supported")


# Ensure required folders exist, validate input folders
base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
safe_pic = os.path.join(base, "pic")
safe_secret = os.path.join(base, "pic", "secret")

os.makedirs(safe_pic, exist_ok=True)
os.makedirs(safe_secret, exist_ok=True)

# Read env input folders once
input_folder = os.getenv("PICTURES_INPUT_FOLDER")
secret_input_folder = os.getenv("SECRET_PICTURES_INPUT_FOLDER")

errors = []

# Validate env folders exist
for name, folder in [
    ("PICTURES_INPUT_FOLDER", input_folder),
    ("SECRET_PICTURES_INPUT_FOLDER", secret_input_folder),
]:
    if not folder or not os.path.isdir(folder):
        errors.append(f"{name} is missing or invalid: {folder}")

# Normalize paths
def norm(p):
    return os.path.abspath(p) if p else None

safe_paths = {norm(safe_pic), norm(safe_secret)}

# Ensure input folders are not destination folders
for name, folder in [
    ("PICTURES_INPUT_FOLDER", input_folder),
    ("SECRET_PICTURES_INPUT_FOLDER", secret_input_folder),
]:
    if norm(folder) in safe_paths:
        errors.append(f"{name} must not point to destination folders: {folder}")

if errors:
    logger.error(f"Startup validation failed: {errors}")
    raise SystemExit(1)


def process_image_folder(src_folder: str, dest_folder: str):
    if not src_folder or not os.path.isdir(src_folder):
        logger.warning(f"Input folder missing or invalid: {src_folder}")
        return

    os.makedirs(dest_folder, exist_ok=True)

    for filename in os.listdir(src_folder):
        src_path = os.path.join(src_folder, filename)

        if not os.path.isfile(src_path):
            continue

        try:
            with Image.open(src_path) as img:
                img.verify()

            with Image.open(src_path) as img:
                img = img.convert("RGB")
                base_name = os.path.splitext(filename)[0]

                dest_path = os.path.join(dest_folder, base_name + ".jpg")
                i = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(dest_folder, f"{base_name}_{i}.jpg")
                    i += 1

                img.save(dest_path, "JPEG", quality=90)

            os.remove(src_path)
            logger.info(f"Processed and moved image: {filename} -> {dest_path}")

        except UnidentifiedImageError:
            logger.warning(f"Rejected non-image file: {filename}")
            # Optionally: move instead of delete
            os.remove(src_path)

        except Exception as e:
            logger.error(f"Failed processing {filename}: {e}")


def import_all_images():
    logger.info("Starting image import process")

    process_image_folder(input_folder, safe_pic)
    process_image_folder(secret_input_folder, safe_secret)

    logger.info("Image import process completed")


@bot.event
async def on_ready():
    if not daily_pistouche.is_running():
        import_all_images()
        daily_pistouche.start()
        logger.info("DogBot9000 up and running")
