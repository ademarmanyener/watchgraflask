# -*- encoding: utf-8 -*-
from includes import *
from PIL import Image

# def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    # x, y = im.size
    # size = max(min_size, x, y)
    # new_im = Image.new('RGBA', (size, size), fill_color)
    # new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    # return new_im

# this class is made for image upload
class CustomFormComponent:
    def upload_file(upload_file, save_folder_path, file_type='poster'):
        _tmp_secureFilename = secure_filename(upload_file.filename)
        _tmp_generatedFilename = file_type + '.jpg'
        upload_file.save(os.path.join(save_folder_path, _tmp_generatedFilename)) 

        if file_type == 'poster' or file_type == 'avatar':
            _GET_HEIGHT = 240 
        elif file_type == 'background':
            _GET_HEIGHT = 720 
        else:
            _GET_HEIGHT = 360 

        try: UploadImageResize(image=os.path.join(save_folder_path, _tmp_generatedFilename)).resize_and_save(get_height=_GET_HEIGHT)
        except: pass
        return

class UploadImageResize:
    IMAGE = None 
    def __init__(self, image:str):
        self.IMAGE = image

    def resize_and_save(self, get_width:int=None, get_height:int=None):
        img = Image.open(self.IMAGE)
        width, height = img.size
        #### for WIDTH
        if get_width:
            new_width = get_width
            new_height = round(new_width * height / width)
        #### for HEIGHT 
        elif get_height:
            new_height = get_height
            new_width = round(new_height * width / height)
        #### or default: WIDTH 300
        else:
            new_width = 300 
            new_height = round(new_width * height / width)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save(self.IMAGE)
        return 

    # ! DOESN'T WORK AT ALL
    def make_square_and_save(self, min_size=256, fill_color=(0, 0, 0, 0)):
        img = Image.open(self.IMAGE)
        x, y = img.size
        size = max(min_size, x, y)
        new_img = Image.new('RGBA', (size, size), fill_color)
        new_img.paste(img, (int((size - x) / 2), int((size - y) / 2)))
        img.save(self.IMAGE)
