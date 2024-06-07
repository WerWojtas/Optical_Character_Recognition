import cv2
from ocr.pattern_finder import PatternFinder
from creators.font_creator import FontCreator
from copy import deepcopy
from PIL import Image
import os
import numpy as np


class OCR():
    def __init__(self):
        self.letter_order = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                             'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3',
                             '4', '5', '6', '7', '8', '9', '?', '!', ',', '.']
        self.save_order = deepcopy(self.letter_order)
        self.creator = FontCreator()
        self.pattern_finder = PatternFinder()
        self.letters = None
        self.all_text = None
        self.spacing = None
        self.font_name = None
        self.letter_width = 0
        self.letter_height = 0

    def upload_font(self, font_name, font_size, spacing, sensitivity=0.98):
        self.font_name = font_name
        self.font_size = font_size
        self.spacing = spacing
        self.letter_order = self.save_order
        self.letters, self.all_text = self.creator.create_font(font_name, font_size)
        self.get_letter_order(self.font_size, sensitivity)
        self.letter_width = 0
        self.letter_height = 0
        for letter in self.letter_order:
            self.letter_width += self.letters[letter].shape[1]
            if self.letter_height < self.letters[letter].shape[0]:
                self.letter_height = self.letters[letter].shape[0]
        self.letter_width = self.letter_width / len(self.letter_order)


    def get_letter_order(self, font_size, sensitivity):
        text = deepcopy(self.all_text)
        text = np.array(text)
        text = cv2.bitwise_not(text)
        _, letter_number = self.find_letters(text, font_size,sensitivity, noise=False, remove=False, use_sensitivity=False)
        sorted_letter_number = sorted(letter_number.items(), key=lambda x: x[1])
        self.letter_order = [x[0] for x in sorted_letter_number if x[0] != '.']
        self.letter_order.append('.')

    def clue_with_font(self, image):
        width1, height1 = image.size
        width2, height2 = self.all_text.size
        final_width = max(width1, width2)
        final_height = height1 + height2
        final_image = Image.new('L', (final_width, final_height), color='white')
        final_image.paste(self.all_text, (0, 0))
        final_image.paste(image, (0, height2))
        return final_image

    def image_to_text(self, image, sensitivity=0.98, noise=False):
        image_copy = deepcopy(image)
        image = self.clue_with_font(image)
        image = np.array(image)
        image = cv2.bitwise_not(image)
        letters, numbers  = self.find_letters(image, self.font_size, sensitivity, noise)
        letters = self.split_to_lines(letters, np.array(image_copy))
        letters = sorted(letters, key=lambda x: (x[1], x[2]))
        text = ''
        last = 0
        for i in range(len(letters)-1):
            letter, line ,place = letters[i]
            letter2, line2, place2 = letters[i+1]
            if letter == letter2 and line == line2 and place2 - place < self.letters[letter].shape[1]//2 or line <= 0:
                continue
            if line != last and line != 1:
                text += '\n'
                last = line
            if place2- self.letters[letter2].shape[1] - place > self.spacing*self.letter_height:
                text += letter
                text += ' '
            else:
                text += letter
        text += letters[-1][0]
        return text
    
    def split_to_lines(self, results, image):
        height = image.shape[0]
        lines = (height-20) // (self.letter_height)
        if lines == 0:
            line_height = height
        else:
            line_height = height // lines
        a_height = self.letters['a'].shape[0]
        for k in range(len(results)):
            letter, i, j = results[k]
            line = (i-(a_height//2)) // line_height
            results[k] = (letter, line, j)
        return results

    def find_letters(self, image,font_size, sensitivity, noise, remove=True, use_sensitivity=True):
        letter_number = {}
        result = []
        for letter in self.letter_order:
            pattern = cv2.bitwise_not(self.letters[letter])
            sens = self.get_sensitivity(self.font_name,letter, sensitivity, noise) if use_sensitivity == True else sensitivity
            correlation = self.pattern_finder.find_pattern(image, pattern, sens)
            letter_number[letter] = 0
            for i,j in zip(*np.where(correlation > 0)):
                if remove:
                    if font_size < 35:
                        image[i-pattern.shape[0]+1:i+1, j-pattern.shape[1]+1:j] = 0
                    else:
                        image[i-pattern.shape[0]+1:i+1, j-pattern.shape[1]+1:j-1] = 0
                letter_number[letter] += 1
                result.append((letter, i, j))
        return result, letter_number

    
    def get_sensitivity(self, font_name, letter, sensitivity, noise):
        if noise:
            if font_name == 'fonts/times.ttf': 
                if letter in ['n','i']:
                    return 0.95
                if letter in ['t']:
                    return 0.85
            return sensitivity
        if font_name == 'fonts/arial.ttf':
            if letter in ['?']:
                return 0.99
            return sensitivity
        if font_name == 'fonts/times.ttf':
            if letter in ['t','n','r']:
                return 0.96
            if letter in ['o']:
                return 0.95
            if letter in ['.']:
                return 0.99
            return sensitivity
        return sensitivity