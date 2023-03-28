from builtins import bytes
from io import BytesIO
from pathlib import Path
from PIL import Image
import math

def  sizing_adjust(image: Image.Image) -> Image.Image:
    width, height = image.size    
    if width > height:
        larger_side, side = width, 'w'
    elif width < height:
        larger_side, side = height, 'h'
    else:
        larger_side, side = width, 's'

    num_pow = math.ceil(math.log(larger_side, 2))
    if num_pow > 13:
        num_pow = 13
    convert_length = pow(2, num_pow)
    
    converter = {
        'w': (convert_length, math.ceil(height/width * convert_length)),
        'h': (math.ceil(width/height *convert_length), convert_length),
        's': (convert_length, convert_length)
        }
    convert_to = converter.get(side)
    return image.resize(convert_to)


def generate(image :Image.Image, outpath: Path, zoom_level: int, resize_width: int):
    """
    generates map tiles from large image
    """

    # how many tiles will that be?
    num_tiles = pow(2, zoom_level)

    width, height = image.size    

    #Tile size calculation
    max_length = max(width, height)
    tile_width = int(math.ceil(max_length / num_tiles))

    # create output directory
    outpath.mkdir(exist_ok=True)
    outpath = outpath.joinpath(str(zoom_level))
    outpath.mkdir(exist_ok=True)

    # Remove existing children
    for child in outpath.rglob('*.png'):
        child.unlink()

    # Croping tile with PIL,  All blank tiles will not be create
    for x in range(num_tiles):
        outpath.joinpath(str(x)).mkdir(exist_ok=True)
        for y in range(num_tiles):
            left = tile_width * x
            top = tile_width * y
            right = left + tile_width
            bottom = top + tile_width
            if top > image.height or left > image.width:
                break
            tile = image.crop([left, top, right, bottom])
            tile = tile.resize([resize_width, resize_width])
            tile_path = outpath.joinpath(f'{x}/{y}.png')
            tile.save(tile_path)

def img2tiles(image: Image.Image, zoom_min: int, zoom_max: int, output_path: Path, resize_width = 256):
    image = sizing_adjust(image)
    for z in range(zoom_min, zoom_max+1):
        generate(image, output_path, z, resize_width)
