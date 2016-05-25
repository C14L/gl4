import shutil
from django.conf import settings
from django.core.management.base import BaseCommand
from os.path import join, isfile, exists
from random import randint

from stonedb.models import Texture, Color, Classification, Country, Stone

"""
Find one stone picture for each possible search option combination and copy it
to "stoneimages/country-texture-color-classifiction.jpg", for example
  - stoneimages/canada-medium-grained-grey-anorthosite.jpg
  - stoneimages/veined-green-marble.jpg
  - stoneimages/brail-blue.jpg
  - stoneimages/coarse-grained-granite.jpg
  - stoneimages/grey-limestone.jpg
etc.
"""


sd = 'stonedb/stonesimages'
src_dir = join(settings.BASE_DIR, sd, 'stonespics')
trg_dir = join(settings.BASE_DIR, sd, 'stonesbrowse')


def copy_stone_pic(stone, kv):
    order = ['country', 'texture', 'color', 'classification']
    kvd = dict(kv)
    src_fn = stone.get_pic_fname()
    trg_fn = '{}.jpg'.format('-'.join([kvd[x] for x in order if x in kvd]))

    # print('{} --> {}'.format(src_fn, trg_fn))

    src = join(src_dir, src_fn)
    trg = join(trg_dir, trg_fn)

    # Do not overwrite existing!
    if exists(trg):
        print('o', end='', flush=True)
        return True

    try:
        shutil.copy(src, trg)
        print('.', end='', flush=True)
        return True
    except FileNotFoundError:
        print('E', end='', flush=True)
        return False


def get_random_stone(stones_qs):
    count = stones_qs.count()
    if count < 1:
        return None
    stone = None
    for i in range(5):
        idx = randint(0, count - 1)
        stone = stones_qs[idx]
        fn = stone.get_pic_fname()
        src = join(src_dir, fn)
        if isfile(src):
            break
    return stone


def make_props(props, stones_qs=None, stones_kv=None):
    if stones_qs is None and stones_kv is None:
        stones_qs = Stone.objects.all()
        stones_kv = []

    my_props = props.copy()
    keyname, qs = my_props.popitem()

    for item in qs:
        this_qs = stones_qs.filter(**{keyname: item})
        this_kv = stones_kv + [(keyname, item.slug)]

        if len(my_props) > 0:
            make_props(my_props, this_qs, this_kv)
        else:
            stone = get_random_stone(this_qs)
            if stone:
                copy_stone_pic(stone, this_kv)


class Command(BaseCommand):
    args = ""
    help = ('Copy one stone picture for each possible search option combination'
            ' to "stoneimages/country-texture-color-classifiction.jpg".')

    def handle(self, *args, **options):
        # make_props({'country': Country.objects.all()})
        # make_props({'color': Color.objects.all()})
        # make_props({'classification': Classification.objects.all()})
        # make_props({'texture': Texture.objects.all()})

        make_props({
            'classification': Classification.objects.all(),
            'color': Color.objects.all(),
            'country': Country.objects.all(),
            'texture': Texture.objects.all(),
        })
