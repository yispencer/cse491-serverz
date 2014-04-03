# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup(): # stuff that should be run once.
    html.init_templates()

    i1 = open('images/1.jpg', 'rb').read()
    img1 = image.add_image_metadata(i1, "meme1", "typical meme")
    image.add_image(img1)
    i2 = open('images/2.jpg', 'rb').read()
    img2 = image.add_image_metadata(i2, "meme2", "challenge accepted")
    image.add_image(img2)

def teardown(): # stuff that should be run once.
    pass
