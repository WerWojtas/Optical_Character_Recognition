
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

class FontCreator():
    def __init__(self):
        self.letter_order = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                             'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3',
                             '4', '5', '6', '7', '8', '9', '?', '!', ',', '.']
        
        
    def create_font(self, font_name, font_size):
        letters = {}
        font = ImageFont.truetype(font_name, font_size)
        all_text = ""
        for letter in self.letter_order:
            text = letter
            image = Image.new('L', (1000, 1000), color='black')
            draw = ImageDraw.Draw(image)
            draw.text((10, 10), text, font=font, fill='white')
            image = image.crop(image.getbbox())
            image = ImageOps.invert(image)
            all_text += letter
            letters[letter] = np.array(image)
        image = Image.new('L', (10000, 1000), color='black')
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), all_text, font=font, fill='white')
        image = image.crop(image.getbbox())
        image = ImageOps.invert(image)
        return letters, image