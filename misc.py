try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

#~ from PIL import Image
#~ from PIL import ImageEnhance
from random import randrange
import re
import base64


#~ Image.preinit()
#~ Image._initialized = 2


DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = "%s %s" %(DATE_FORMAT, TIME_FORMAT)



def image_resize_image(base64_source, size=(1024, 1024), encoding='base64', filetype=None, avoid_if_small=False):
    if not base64_source:
        return False
    if size == (None, None):
        return base64_source
    image_stream = StringIO.StringIO(base64_source.decode(encoding))
    image = Image.open(image_stream)
    # store filetype here, as Image.new below will lose image.format
    filetype = (filetype or image.format).upper()

    filetype = {
        'BMP': 'PNG',
    }.get(filetype, filetype)

    asked_width, asked_height = size
    if asked_width is None:
        asked_width = int(image.size[0] * (float(asked_height) / image.size[1]))
    if asked_height is None:
        asked_height = int(image.size[1] * (float(asked_width) / image.size[0]))
    size = asked_width, asked_height

    # check image size: do not create a thumbnail if avoiding smaller images
    if avoid_if_small and image.size[0] <= size[0] and image.size[1] <= size[1]:
        return base64_source

    if image.size != size:
        image = image_resize_and_sharpen(image, size)
    if image.mode not in ["1", "L", "P", "RGB", "RGBA"] or (filetype == 'JPEG' and image.mode == 'RGBA'):
        image = image.convert("RGB")

    background_stream = StringIO.StringIO()
    image.save(background_stream, filetype)
    return background_stream.getvalue().encode(encoding)

def isBase64(string):
    return (len(string) % 4 == 0) and re.match('^[A-Za-z0-9+/]+[=]{0,2}$', string)

def encode_image(data):
    return base64.encodestring(data)
    
