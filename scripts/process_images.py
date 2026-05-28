from pathlib import Path
from PIL import Image
import re

BASE_DIR = Path(__file__).resolve().parent.parent

ORIGINALS_DIR = BASE_DIR / "images" / "Originals"
LARGE_DIR = BASE_DIR / "images" / "Large"
THUMBS_DIR = BASE_DIR / "images" / "Thumbs"

LARGE_MAX_WIDTH = 1200
THUMB_MAX_WIDTH = 300
JPEG_QUALITY = 82

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def resize_image(source_path, output_path, max_width, square_crop=False):
    with Image.open(source_path) as img:
        img = img.convert("RGB")

        width, height = img.size
        original_width = width
        original_height = height

        # Resize proportionally
        if width > max_width:
            new_height = int(height * max_width / width)
            img = img.resize((max_width, new_height), Image.LANCZOS)

        # Square crop from center
        # Square crop from center
        # Crop from center, with optional x/y shift and optional w/h expansion
        if square_crop:
            width, height = img.size
            base_crop_size = min(width, height)

            offset_x, offset_y, extra_width, extra_height = get_crop_settings(source_path.name)

            scale_x = width / original_width
            scale_y = height / original_height

            offset_x = int(offset_x * scale_x)
            offset_y = int(offset_y * scale_y)
            extra_width = int(extra_width * scale_x)
            extra_height = int(extra_height * scale_y)

            crop_width = base_crop_size + extra_width
            crop_height = base_crop_size + extra_height

            # Keep crop dimensions valid
            crop_width = max(1, min(crop_width, width))
            crop_height = max(1, min(crop_height, height))

            left = (width - crop_width) // 2 + offset_x
            top = (height - crop_height) // 2 + offset_y

            # Keep crop box inside image boundaries
            left = max(0, min(left, width - crop_width))
            top = max(0, min(top, height - crop_height))

            right = left + crop_width
            bottom = top + crop_height

            img = img.crop((left, top, right, bottom))

        img.save(output_path, "JPEG", quality=JPEG_QUALITY, optimize=True)

def get_crop_settings(filename):
    """
    Reads optional crop settings from filenames like:

    jp-kawaguchiko-bridge-01-y-80.jpg
    jp-tokyo-flower-01-x+50-y-30.jpg
    jp-uji-drain-01-w+100.jpg
    jp-uji-drain-01-w+100-y-30.jpg

    x / y shift the crop center.
    w / h expand the crop box width or height before resizing.
    """
    offset_x = 0
    offset_y = 0
    extra_width = 0
    extra_height = 0

    filename = filename.lower()

    x_match = re.search(r"-x([+-]\d+)", filename)
    y_match = re.search(r"-y([+-]\d+)", filename)
    w_match = re.search(r"-w([+-]\d+)", filename)
    h_match = re.search(r"-h([+-]\d+)", filename)

    if x_match:
        offset_x = int(x_match.group(1))

    if y_match:
        offset_y = int(y_match.group(1))

    if w_match:
        extra_width = int(w_match.group(1))

    if h_match:
        extra_height = int(h_match.group(1))

    return offset_x, offset_y, extra_width, extra_height

def clean_output_name(source_path):
    stem = source_path.stem

    # Remove crop/offset modifiers at the end of the filename
    # Handles: --x+50, --x-50, -x+50, -x-50
    stem = re.sub(r"(-{1,2}x[+-]\d+)$", "", stem)

    return stem + ".jpg"

def main():
    LARGE_DIR.mkdir(parents=True, exist_ok=True)
    THUMBS_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old generated files
    for folder in [LARGE_DIR, THUMBS_DIR]:
        for file in folder.iterdir():
            if file.is_file():
                file.unlink()

    image_files = [
        file for file in ORIGINALS_DIR.iterdir()
        if file.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if not image_files:
        print(f"No images found in {ORIGINALS_DIR}")
        return

    for source_path in image_files:
        output_name = clean_output_name(source_path)

        large_path = LARGE_DIR / output_name
        thumb_path = THUMBS_DIR / output_name

        print(f"Processing {source_path.name}")

        resize_image(source_path, large_path, LARGE_MAX_WIDTH, square_crop=True)
        resize_image(source_path, thumb_path, THUMB_MAX_WIDTH, square_crop=True)



    print(f"Processed {len(image_files)} images.")
    print("Done.")


if __name__ == "__main__":
    main()