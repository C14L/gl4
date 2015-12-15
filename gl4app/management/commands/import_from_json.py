import json
from datetime import datetime
from os import rename
from os.path import join, isfile, dirname
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils.text import slugify
from django.utils.timezone import utc
from companydb.models import (UserProfile, )
from stonedb.models import (Stone, StoneName, Color, Classification,
                            Texture, Country)


def parse_iso_datetime(t):
    """Return timezone aware datetime from simple 'yyyy-mm-dd hh-mm-ss'."""
    try:
        return datetime.strptime(t, "%Y-%m-%d %H:%M:%S").replace(tzinfo=utc)
    except:
        return datetime.utcnow().replace(tzinfo=utc)


class Command(BaseCommand):
    args = ""
    help = "Import most old Graniteland data from JSON files."
    data_dir = join(dirname(settings.BASE_DIR), 'import_data')
    pics_dir = join(settings.BASE_DIR, 'stonedb/stonesimages')
    lang = 'en'

    def handle(self, *args, **options):
        print(
            '\nThis will import all old Graniteland data JSON files.\n\n'
            '1. Import colors, classifications, countries.\n\n'
            '2. Import user accounts.\n\n'
            '3. Import profiles and group relations.\n\n'
            '4. Import stones and stone pictures, renaming jpg files.\n\n'
            '5. WONT: (mostly spam anyway) ~~Import user stock items~~.\n\n'
            '6. WONT: (mostly spam anyway) ~~Import user showroom items~~.\n\n'
            '7. Import user uploaded pictures, keeping relation to profiles, '
            'stones, stock items, showroom item.\n\n'
            )
        input('Please press Enter to continue...')

        self.import_color()
        self.import_classification()
        self.import_country()
        self.import_user()
        self.import_stone()

    def walkjsondata(self, fn):
        f = join(self.data_dir, '{}__{}.json'.format(self.lang, fn))
        with open(f) as fh:
            for line in fh:  # MySQL adds different kind of comments to the
                if line.startswith('['):  # data file. Find actual JSON data.
                    break
        for row in json.loads(line):
            yield row

    def import_color(self):
        Color.objects.all().delete()
        for row in self.walkjsondata('data_colors'):
            item = Color.objects.create(
                id=row['id'], slug=row['url'], name=row['name'])
            print('color --> added: {} {} -> {}'.format(
                item.id, item.slug, item.name))

    def import_classification(self):
        """
        {"id":"1","old_class":"amazonit - granit","name":"Amazonite
        Granite","url":"amazonitegranit","simple":"Granite"}
        """
        Classification.objects.all().delete()
        for row in self.walkjsondata('data_stone_classifications'):
            item = Classification.objects.create(
                id=row['id'], slug=row['url'], name=row['name'],
                simple_slug=slugify(row['simple']), simple_name=row['simple'])
            print('classif --> added: {} {} -> {}'.format(
                item.id, item.slug, item.name))

    def import_country(self):
        # {"un3":"4","iso2":"af","url":"afghanistan","name":"Afghanistan"}
        Country.objects.all().delete()
        for row in self.walkjsondata('data_country_names'):
            item = Country.objects.create(id=row['un3'], cc=row['iso2'],
                                          slug=row['url'], name=row['name'])
            print('country --> added: {} [{}] {} -> {}'.format(
                item.id, item.cc, item.slug, item.name))

    def import_user(self):
        """

        --- user --------------------------------------------------------------
        {"user_id":"22","nick":"YYY","pass":"XXX","email":"info@example.com",
        "name":"Blah Corp.","type":"company","title_foto":"12","title_foto_ext"
        :"jpg","time_offset":"0","datetime_format":"Y-m-d H:i:s",
        "date_short":"Y-m-d","date_long":"l, d F Y","signup_ip":"0.0.0.0",
        "signup_time":"2005-06-12 08:48:07","lastlogin_ip":"0.0.0.0",
        "lastlogin_time":"2008-08-17 02:40:28","lastlogout_time":
        "2008-08-17 02:40:28","is_blocked":"0","is_deleted":"0","is_readonly":
        "0","is_admin":"0","is_mod_global":"0","is_mod_forum":"0",
        "is_mod_fotos":"0","is_mod_stones":"0","is_mod_pages":"0",
        "is_mod_groups":"0","is_mod_tradeshows":"0"}
        --- profile -----------------------------------------------------------
        {"user_id":"1","nick":"admin","name":"Graniteland","contact":
        "xxxxxxx","contact_position":"","slogan":"","street":"","city":"",
        "zip":"","country_sub_id":"0","country_id":"0","country_sub_name":"",
        "country_name":"","postal":"","email":"info@graniteland.com","fax":"",
        "tel":"","mobile":"","web":"","about":"","title_foto":"0",
        "title_foto_ext":""}
        -----------------------------------------------------------------------

        """
        User.objects.all().delete()
        UserProfile.objects.all().delete()
        for row in self.walkjsondata('user'):
            repr(row)

            print('user --> adding {} [{}] --> {}'.format(
                row['nick'], row['user_id'], row['name']))

            try:
                user = User(id=row['user_id'])
                user.username = row['nick']
                user.set_password(row['pass'])
                user.email = row['email']
                user.last_login = parse_iso_datetime(row['lastlogin_time'])
                user.date_joined = parse_iso_datetime(row['signup_time'])
                user.save()
            except IntegrityError as e:
                print('!!! IntegrityError: {}'.format(e))
                continue

            profile = UserProfile.objects.create(user=user)
            profile.name = row['name']
            profile.title_foto = row['title_foto']
            profile.title_foto_ext = row['title_foto_ext']
            profile.signup_ip = row['signup_ip']
            profile.lastlogin_ip = row['lastlogin_ip']
            profile.is_blocked = bool(row['is_blocked'])
            profile.is_deleted = bool(row['is_deleted'])
            profile.save()

            print('--> User added: {} {}'.format(user.id, user.username))

    def import_stone(self):
        Stone.objects.all().delete()
        StoneName.objects.all().delete()
        urlname_changes = []
        for row in self.walkjsondata('stones'):
            stone = Stone.objects.create(id=row['id'], name=row['name'])
            stone.slug = slugify(row['name'])
            stone.urlname = row['urlname']  # old urlname value
            stone.city_name = row['city']
            stone.application = row['application']
            stone.availability = row['availability']
            stone.comment = row['comment']
            stone.maxsize = row['maxsize']

            stone.color_name = row['color']
            stone.country_name = row['country']
            stone.classification_name = row['classification']
            stone.texture_name = row['texture']

            stone.secondary_colors = []
            stone.texture = Texture.objects.filter(
                pk=row['texture_id']).first()
            stone.classification = Classification.objects.filter(
                pk=row['classification_id']).first()
            stone.color = Color.objects.filter(
                pk=row['color_id']).first()
            stone.country = Country.objects.filter(
                pk=row['country_id']).first()

            stone.save()

            # check if item was using smallpic, largepic, projectpic or
            # title_foto and is_use_title_foto fields.
            fname = stone.get_pic_fname()
            sf_indx = join(self.pics_dir, 'stonesindex', row['smallpic'])
            sf_pics = join(self.pics_dir, 'stonespics', row['largepic'])
            tf_indx = join(self.pics_dir, 'stonesindex', fname)
            tf_pics = join(self.pics_dir, 'stonespics', fname)

            if isfile(sf_indx):
                print('{} --> {}'.format(sf_indx, tf_indx))
                rename(sf_indx, tf_indx)
            else:
                print('FILE NOT FOUND: {}'.format(sf_indx))

            if isfile(sf_pics):
                print('{} --> {}'.format(sf_pics, tf_pics))
                rename(sf_pics, tf_pics)
            else:
                print('FILE NOT FOUND: {}'.format(sf_pics))

            # Fill StoneName pseudonym table; add the main name too!
            StoneName.objects.create(stone=stone, name=stone.name,
                                     slug=stone.slug)
            for x in row['pseudonym'].split(', '):
                x = x.strip(' \t\n\r,;.')
                if x:
                    StoneName.objects.create(stone=stone, name=x,
                                             slug=slugify(x))

            print('{} {}: {} --> {}'.format(
                stone.id, stone.slug, stone.name, fname))

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
