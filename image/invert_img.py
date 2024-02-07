import argparse

from pathlib import Path
from PIL import Image
import PIL.ImageOps

parser = argparse.ArgumentParser(description="Invert colors of image.")
parser.add_argument("--path", "-p", type=str, required=True, help="path to image")
args = parser.parse_args()


target_path = Path(args.path)
new_path = target_path.parent / f"{target_path.stem}_neg{target_path.suffix}"

image = Image.open(target_path).convert('RGB')
inverted_image = PIL.ImageOps.invert(image)

inverted_image.save(new_path)
