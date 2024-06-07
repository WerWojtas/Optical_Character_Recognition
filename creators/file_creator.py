from PIL import Image, ImageDraw, ImageFont, ImageOps
import cv2
import os
import numpy as np

class FileCreator:
    def __init__(self, files_path = 'images/'):
        self.files_path = files_path

    def create_text(self,text, font_name, font_size, file_name):
        image = Image.new('L', (10000, 10000), color='black')
        text = text.split('\n')
        for i, line in enumerate(text):
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(font_name, font_size)
            draw.text((10, 10 + i*font_size), line, font=font, fill='white')
        image = image.crop(image.getbbox())
        image = ImageOps.invert(image)
        image = ImageOps.expand(image, border=10, fill='white')
        image.save(f'{self.files_path}{file_name}.png')

    def rotate_PIL(self,image_path, angle):
        image = Image.open(image_path)
        image = image.rotate(angle, expand=1, fillcolor='white')
        image.save(image_path)

    def add_noise(self,file_path, noise):
        img = Image.open(file_path)
        img = np.array(img)
        noise = np.random.normal(0, noise, img.shape)
        noisy = img + noise
        noisy = np.clip(noisy, 0, 255)
        image =  Image.fromarray(noisy.astype(np.uint8))
        image.save(file_path)