import os
import itertools
from PIL import Image


def change_name(instance, filename):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)

    new_path = f'product/{instance.pk}{ext}'
    return new_path


def mygrouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e != None] for t in itertools.zip_longest(*args))


def change_image_size(path, x_size, y_size):
    output_size = (x_size, y_size)
    image = Image.open(path)
    image = image.resize(output_size)
    return image


def remove_exif_data(path):
    with Image.open(path) as f:
        f.getexif().clear()
        f.save(f, image_file.content_type)
    return f
