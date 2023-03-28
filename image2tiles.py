#!/usr/bin/env python3
"""
Inspired by 
"https://github.com/danizen/campaign-map/blob/master/gentiles.py" 
and 
"https://github.com/bramus/photoshop-google-maps-tile-cutter/blob/master/PS_Bramus.GoogleMapsTileCutter.jsx"

Takes a large image as the input, outputs map tiles
at the appropriate size and file structure for use
in frameworks like leaflet.js, MapBox, etc.

DETAILS:
Resulting tiles are 256px square, regardless of the
size of the source image. The number of tiles wide/
high is determined by the "zoom level", which is
2^zoom. In other words, a zoom level of 3 = 8 tiles,
each resized to 256 pixels square.

To handle non-square and non 2^n size, The larger side is lengthen
to the closest 2^n value and the shorter side is lengthen with same ratio
in order to maintain original aspect ratio. The image is sliced base on Bramus
idea, which is sliced down on y axis until no image to slice and then move to next
x value until no image to slice.

Starting position of first tile (0,0) is top left of the image, it can be modify
to other position by calculat new (top, left, right, bottom) which associate with
image full width and height.

Way more info here:
http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Resolution_and_Scale

FILE STRUCTURE
Slippy maps require tiles to be stored in a specific
file structure:
    output_folder/zoom_level/x/y.png

This is the standard arrangement (some frameworks let
you specify others), and should be noted in your Javascript.
For example, if using leaflet.js, you would use:
    tiles/{z}/{x}/{y}.png

"""
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

def img2tiles(bytes: bytes, zoom_min: int, zoom_max: int, output_path: Path, resize_width = 256):
    image = Image.open(BytesIO(bytes))
    image = sizing_adjust(image)
    for z in range(zoom_min, zoom_max+1):
        generate(image, output_path, z, resize_width)