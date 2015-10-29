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
        f = join(dirname(settings.BASE_DIR), 'import_data/en_stone.json')
        urlname_changes = []

        # Get all color, classification, texture, country options.
        color, classification, texture, country = [], [], [], []
        with open(f) as fh:
            for row in json.load(fh):
                if row['color']:
                    x = (int(row['color_id']), row['color'])
                    if x not in color:
                        color.append(x)
                if row['classification']:
                    x = (int(row['classification_id']), row['classification'])
                    if x not in classification:
                        classification.append(x)
                if row['texture']:
                    x = (int(row['texture_id']), row['texture'])
                    if x not in texture:
                        texture.append(x)
                if row['country']:
                    x = (int(row['country_id']), row['country'])
                    if x not in country:
                        country.append(x)

        print('\n\n======================================================\n\n')
        print(color)
        print('\n\n======================================================\n\n')
        print(classification)
        print('\n\n======================================================\n\n')
        print(texture)
        print('\n\n======================================================\n\n')
        print(country)
        print('\n\n======================================================\n\n')

        input('PRESS ENTER TO START INPUT...')

        print('Truncating Stone, StoneName tables...')
        Stone.objects.all().delete()
        StoneName.objects.all().delete()
        print('done.')

        with open(f) as fh:
            for row in json.load(fh):
                stone, created = Stone.objects.get_or_create(id=row['id'])
                stone.name = row['name']
                stone.slug = slugify(row['name'])
                stone.urlname = row['urlname']  # old urlname value
                stone.country = row['country_id']
                stone.country_name = row['country']
                stone.city_name = row['city']
                stone.application = row['application']
                stone.availability = row['availability']
                stone.comment = row['comment']
                stone.maxsize = row['maxsize']
                stone.color = row['color_id']
                # stone.secondary_colors = Stone.COLOR_CH
                stone.classification = row['classification_id']
                # stone.texture = Stone.TEXTURE_CH
                # stone.simpletype = Stone.SIMPLETYPE_CH
                stone.save()

                # stone.picfile --> create standard filename for pic and thumb.
                # check if item was using smallpic, largepic, projectpic or
                # title_foto and is_use_title_foto fields.

                # Fill StoneName pseudonym table
                for x in row['pseudonym'].split(', '):
                    StoneName.objects.create(
                        stone=stone, name=x, slug=slugify(x))

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
