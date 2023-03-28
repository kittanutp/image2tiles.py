# Image2Tiles

Takes a large image as the input, outputs map tiles
at the appropriate size and file structure for use
in frameworks like leaflet.js, MapBox, etc.

## DEPENDENCIES

This code is written by intention of repalcement on gdal2tiles.py on non-geographic image (ex floor plan)
It is writen by mostly native python library.

## INSPIRED BY

https://github.com/danizen/campaign-map/blob/master/gentiles.py and https://github.com/bramus/photoshop-google-maps-tile-cutter/blob/master/PS_Bramus.GoogleMapsTileCutter.jsx

## DETAILS

Resulting tiles are 256px square, regardless of the size of the source image. The number of tiles wide high is determined by the "zoom level", which is
2^zoom. In other words, a zoom level of 3 = 8 tiles, each resized to 256 pixels square.

To handle non-square and non 2^n size, The larger side is lengthen to the closest 2^n value and the shorter side is lengthen with same ratio
in order to maintain original aspect ratio. The image is sliced base on Bramus idea, which is sliced down on y axis until no image to slice and then move to next
x value until no image to slice.

Starting position of first tile (0,0) is top left of the image, it can be modify to other position by calculat new (top, left, right, bottom) which associate with
image full width and height.

## TECHNICAL INFO

http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Resolution_and_Scale

## FILE STRUCTURE

Slippy maps require tiles to be stored in a specific
file structure:
    output_folder/zoom_level/x/y.png

This is the standard arrangement (some frameworks let
you specify others), and should be noted in your Javascript.
For example, if using leaflet.js, you would use:
    tiles/{z}/{x}/{y}.png
## TO USE

```python
image = Image.open('your_image.png')
out_path = Path('output_folder')
img2tiles(image, 0, 5, out_path)
```
