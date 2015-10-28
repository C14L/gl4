import json
from os.path import join, dirname
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from stonedb.models import Stone, StoneName


class Command(BaseCommand):
    args = ""
    help = "Simple import for old stone data from JSON file."

    def handle(self, *args, **options):
        urlname_changes = []
        print('Truncating Stone, StoneName tables...')
        Stone.objects.all().delete()
        StoneName.objects.all().delete()
        print('done.')
        f = join(dirname(settings.BASE_DIR), 'import_data/en_stone.json')
        with open(f) as fh:
            for row in json.load(fh):
                stone, created = Stone.objects.get_or_create(id=row['id'])
                stone.name = row['name']
                stone.slug = slugify(row['name'])
                stone.urlname = row['urlname']  # old urlname value
                stone.country = 0
                stone.country_name = row['country']
                stone.city_name = row['city']
                stone.application = row['application']
                stone.availability = row['availability']
                stone.comment = row['comment']
                stone.maxsize = row['maxsize']
                # stone.color = choices=COLOR_CH
                # stone.secondary_colors = choices=COLOR_CH
                # stone.classification = choices=CLASSIF_CH
                # stone.texture = choices=TEXTURE_CH
                # stone.simpletype = choices=SIMPLETYPE_CH
                stone.save()

                # stone.picfile --> create standard filename for pic and thumb.
                # check if item was using smallpic, largepic, projectpic or
                # title_foto and is_use_title_foto fields.

                print('{} {}: {}'.format(stone.id, stone.slug, stone.name))
                if stone.slug != stone.urlname:
                    urlname_changes.append(
                        'For {}, urlname changed "{}" --> "{}"'.format(
                            stone.id, stone.urlname, stone.slug))

        print('done.')
        print(urlname_changes)
        print('---')

    """
    0   id
    1   name
    2   smallpic
    3   largepic
    4   projectpic
    5   title_foto
    6   is_use_title_foto
    7   country
    8   country_id
    9  city
    10  color
    11  color_id
    12  pseudonym
    13  application
    14  texture
    15  texture_id
    16  availability
    17  maxsize
    18  comment
    19  type_url
    20  classification
    21  classification_id
    22  urlname
    23  update_time datetime
    24  update_ip
    """
