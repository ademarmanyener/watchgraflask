# -*- encoding: utf-8 -*-

# https://auth0.com/blog/image-processing-in-python-with-pillow/
# https://stackoverflow.com/questions/44231209/resize-rectangular-image-to-square-keeping-ratio-and-fill-background-with-black/44231784

from PIL import Image
import sys
import random
import os

# for avatars
def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

img_link = sys.argv[1]
print('{} is opening...'.format(img_link))
test_img = Image.open(img_link)
n_test_img = make_square(test_img, fill_color=(255))
n_test_img = n_test_img.resize((300, 300))
n_test_img = n_test_img.convert('RGB')
#n_test_img.show()
__random_id = random.randint(0, 1024)
n_test_img.save('saved/{}_{}'.format(__random_id, img_link))
os.system('firefox saved/{}_{}'.format(__random_id, img_link))

# for poster or background
## resizing height
# new_width  = 680
# new_height = new_width * height / width 
#
## resizing width
# new_height = 680
# new_width  = new_height * width / height
#
# finally
# img = img.resize((new_width, new_height), Image.ANTIALIAS)
