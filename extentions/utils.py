import os
import itertools

def change_name(instance,filename):
    basename = os.path.basename(filename)
    name,ext = os.path.splitext(basename)

    new_path = f'product/{instance.pk}{ext}'
    return new_path



def mygrouper(n, iterable):
     args = [iter(iterable)] * n
     return ([e for e in t if e != None] for t in itertools.zip_longest(*args))

