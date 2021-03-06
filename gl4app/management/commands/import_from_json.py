import json

import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import IntegrityError
from django.utils.text import slugify
from io import StringIO
from os import rename
from os.path import join, isfile, dirname

from companydb.initial_data import import_company_countries
from companydb.models import Country as Companydb_Country
from companydb.models import (UserProfile, Stock, Project, Pic, Group, Product)
from mdpages.models import Article, Author, Keyword, Topic
from stonedb.models import (Stone, StoneName,
                            Color, Classification, Texture, Country)
from toolbox import parse_iso_date, parse_iso_datetime, force_int
from tradeshowdb.models import Tradeshow


class Command(BaseCommand):
    args = ""
    help = "Import most old Graniteland data from JSON files."
    data_dir = join(dirname(settings.BASE_DIR), 'import_data')
    pics_dir = join(settings.BASE_DIR, 'stonedb/stonesimages')
    LANGUAGE = settings.LANGUAGE_SHORT

    def handle(self, *args, **options):
        print('='*60)
        print('  LANGUAGE: {}'.format(self.LANGUAGE))
        print('  (use GRANITELAND_LANGAUGE=xx environment variable to set it)')
        print('='*60)
        print('''
This will import all old Graniteland data JSON files from the directory:

  BASE_DIR/../import_data/*.json

Begin dumping the old DB as JSON using phpmyadmin, then cut the one large JSON
file into individual files, one per original DB table, using bash/sed/awk:

~$ sed -i.bak -r 's#(// usr_web3_1\\.\\w+)$#\\n\\n\\1\\n\\n#gm' usr_web3_1.json
~$ sed -i.bak3 -z 's/\\n\\n\\n\\n//'g usr_web3_1.json
~$ grep '^\\/\\/\\s*usr_web3_1\\.' usr_web3_1.json | \
      sed -r 's#//\\s*usr_web3_1\\.##; s/\\[/.json>[/1' | \
      awk -F '>' '{for(i=2;i<=NF;i++) print $i >> $1}'

Using the individual JSON files in `import_data/*.json`, this script will

0. Import products, country names for Company model.
1. Import colors, classifications, countries for Stone model.
2. Import user accounts.
3. Import profiles and group relations.
4. Import stones and stone pictures, renaming jpg files.
5. Import user stock and showroom items.
6. Import article pages.
7. Import user uploaded pictures, keeping relation to profiles, stones,
   stock items, showroom item.

        ''')
        input('Please press Enter to continue...')
        self.import_products(force=True)
        self.import_company_countries(force=True)
        self.import_color()
        self.import_classification()
        self.import_country()
        self.init_texture()  # only deletes current entries
        self.import_user()
        self.import_profile()
        self.import_stone()
        self.import_tradeshow()
        self.import_group()
        self.import_stock()
        self.import_projects()
        self.import_pages()
        self.import_pics()  # must be last after Article, Stock, etc.
        self.fix_all_id()

    def walkjsondata(self, fn):
        # line = None
        f = join(self.data_dir, '{}__{}.json'.format(self.LANGUAGE, fn))
        with open(f) as fh:
            for row in json.load(fh, strict=False):
                yield row

        #    for line in fh:  # MySQL adds different kind of comments to the
        #        if line.startswith('['):  # data file. Find actual JSON data.
        #            break
        #if line:
        #    for row in json.loads(line, strict=False):
        #        yield row

    def import_products(self, force=False):
        if force:
            Product.objects.all().delete()
        filename = 'products_{}.txt'.format(self.LANGUAGE)
        filename = join(settings.BASE_DIR, '..', 'fixtures', filename)
        with open(filename) as fh:
            for row in fh:
                row = row.rstrip('\n')
                if not row or row.startswith('#'):
                    continue
                if Product.objects.filter(slug=slugify(row)).first():
                    continue
                Product.objects.create(name=row)

    def import_company_countries(self, force=False):
        import_company_countries(force)

    def import_color(self):
        print('Import colors')
        Color.objects.all().delete()
        for row in self.walkjsondata('data_colors'):
            Color.objects.create(
                id=row['id'], slug=row['url'], name=row['name'])
            print('.', end='', flush=True)
        print('done!')

    def init_texture(self):
        Texture.objects.all().delete()

    def fetch_or_create_texture(self, texture_name):
        # return texture name and id
        texture_name = texture_name.lower().strip()
        tmap = {}
        if texture_name in ['', 'n/a', 'na']:
            return None

        # Fix messed up original data. Valid string values are only
        if self.LANGUAGE == 'en':
            # 'coarse grain', 'medium grain', 'fine grain', 'plain',
            # 'strongly veined', 'medium veined', 'light veined', 'fossiled'
            tmap = {
                'fine grained, with plenty of large fossils': 'fossiled',

                'fine': 'fine grained',
                'fine grain': 'fine grained',
                'fine grained': 'fine grained',
                'fine, veined': 'fine grained',
                'fine grained, veined': 'fine grained',

                'fine, medium': 'medium grained',
                'fine to medium': 'medium grained',
                'medium': 'medium grained',
                'medium - coarse grain': 'medium grained',
                'medium grain': 'medium grained',
                'medium grained': 'medium grained',

                'grob': 'coarse grained',
                'coars': 'coarse grained',
                'coarse': 'coarse grained',
                'coarse grain': 'coarse grained',
                'coarse grained': 'coarse grained',
                'coarse grain, veined': 'coarse grained',

                'geädert': 'veined',
                'veined': 'veined', }

        elif self.LANGUAGE == 'de':
            # 'grobkörnig', 'mittelkörnig', 'feinkörnig', 'gleichförmig',
            # 'stark geädert', 'geädert', 'leicht geädert', 'fossil',
            tmap = {
                'besteht hauptsächlich aus schalen von muscheln und brachioden.': 'fossil',
                'feinkörnig, mit sehr vielen muscheleinschlüssen': 'fossil',
                'feinkörnig, mit vielen fossilen einschlüssen': 'fossil',
                'feinkörnig, mit vielen einschlüssen': 'fossil',
                'teilweise von weißen und grauen fossilien durchsetzt,.': 'fossil',

                'feinkörnig': 'feinkörnig',
                'feinkörnig mit einschlüssen': 'feinkörnig',
                'feinkörnig, mit einschlüssen': 'feinkörnig',
                'feinkörnig grain': 'feinkörnig',
                'feinkörnig grained': 'feinkörnig',
                'feinkörnig mit muscheleinschlüssen': 'feinkörnig',
                'feinkörnig mit großen orthoklas einschlüssen': 'feinkörnig',
                'feinkörnig mit weißen quarzschlieren': 'feinkörnig',

                'star geädert mit großen farbschwankungen': 'stark geädert',

                'feinkörnig, gewolkt': 'geädert',
                'geädert': 'geädert',
                'helles bis weißliches blau mit tiefblauen adern, oft auch große': 'geädert',
                'veined': 'geädert',

                'feinkörnig, geädert': 'leicht geädert',
                'gewolkt': 'leicht geädert',

                'grobkörnig': 'grobkörnig',
                'grobkörning': 'grobkörnig',
                'grob': 'grobkörnig',
                'grobkörnig grain': 'grobkörnig',
                'grobkörnig grain, geädert': 'grobkörnig',
                'grobkörnig grained': 'grobkörnig',
                'grobkörnig, geädert': 'grobkörnig',

                'feinkörnig to mittelkörnig': 'mittelkörnig',
                'feinkörnig, mittelkörnig': 'mittelkörnig',
                'fein- bis mittelkörnig': 'mittelkörnig',
                'mittelkörnig': 'mittelkörnig',
                'mittelkörnig - grobkörnig grain': 'mittelkörnig',
                'mittelkörnig grain': 'mittelkörnig',
                'mittelkörnig grained': 'mittelkörnig', }

        if texture_name in tmap.keys():
            texture_name = tmap[texture_name]
        item, created = Texture.objects.get_or_create(name=texture_name)
        return item

    def import_classification(self):
        """
        {"id":"1","old_class":"amazonit - granit","name":"Amazonite
        Granite","url":"amazonitegranit","simple":"Granite"}
        """
        print('Import classification')
        Classification.objects.all().delete()
        for row in self.walkjsondata('data_stone_classifications'):
            Classification.objects.create(
                id=row['id'], slug=row['url'], name=row['name'],
                simple_slug=slugify(row['simple']), simple_name=row['simple'])
            print('.', end='', flush=True)
        print('done!')

    def import_country(self):
        # {"un3":"4","iso2":"af","url":"afghanistan","name":"Afghanistan"}
        print('Import country')
        Country.objects.all().delete()
        for row in self.walkjsondata('data_country_names'):
            Country.objects.create(id=row['un3'], cc=row['iso2'],
                                   slug=row['url'], name=row['name'])
            print('.', end='', flush=True)
        print('done')

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
        """
        print('Import users and profiles', end='', flush=True)
        User.objects.all().delete()
        UserProfile.objects.all().delete()
        for row in self.walkjsondata('user'):
            if not row['user_id'] or \
                    not row['nick'] or row['type'] != 'company':
                continue
            if int(row['is_deleted']) or int(row['is_blocked']):
                print('D', end='', flush=True)
                continue
            try:
                user = User(id=row['user_id'])
                user.username = row['nick'][:30]
                user.set_password(row['pass'])
                user.email = row['email']
                user.last_login = parse_iso_datetime(row['lastlogin_time'])
                user.date_joined = parse_iso_datetime(row['signup_time'])
                user.save()
            except IntegrityError:
                print('E', end='', flush=True)
                continue
            user.profile.name = row['name']
            user.profile.title_foto = row['title_foto']
            user.profile.title_foto_ext = row['title_foto_ext']
            user.profile.signup_ip = row['signup_ip']
            user.profile.lastlogin_ip = row['lastlogin_ip']
            user.profile.save()
            print('.', end='', flush=True)
        print('done! All users created.')

    def import_stone(self):
        print('Import stones')
        Stone.objects.all().delete()
        StoneName.objects.all().delete()
        urlname_changes = []
        for row in self.walkjsondata('stones'):
            stone = Stone.objects.create(id=row['id'])
            stone.name = row['name']
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
            stone.texture = self.fetch_or_create_texture(row['texture'])
            stone.secondary_colors = []
            stone.color = Color.objects.filter(
                pk=row['color_id']).first()
            stone.classification = Classification.objects.filter(
                pk=row['classification_id']).first()
            stone.country = Country.objects.filter(
                pk=row['country_id']).first()
            stone.save()
            print('.', end='', flush=True)

            # check if item was using smallpic, largepic, projectpic or
            # title_foto and is_use_title_foto fields.
            fname = stone.get_pic_fname()
            sf_indx = join(self.pics_dir, 'stonesindex', row['smallpic'])
            sf_pics = join(self.pics_dir, 'stonespics', row['largepic'])
            tf_indx = join(self.pics_dir, 'stonesindex', fname)
            tf_pics = join(self.pics_dir, 'stonespics', fname)

            if isfile(sf_indx):
                # print('{} --> {}'.format(sf_indx, tf_indx))
                print('i', end='', flush=True)
                rename(sf_indx, tf_indx)
            else:
                # print('FILE NOT FOUND: {}'.format(sf_indx))
                print('x', end='', flush=True)

            if isfile(sf_pics):
                # print('{} --> {}'.format(sf_pics, tf_pics))
                rename(sf_pics, tf_pics)
                print('p', end='', flush=True)
            else:
                # print('FILE NOT FOUND: {}'.format(sf_pics))
                print('x', end='', flush=True)

            # Fill StoneName pseudonym table; add the main name too!
            StoneName.objects.create(stone=stone, name=stone.name,
                                     slug=stone.slug)
            for x in row['pseudonym'].split(', '):
                x = x.strip(' \t\n\r,;.')
                if x:
                    StoneName.objects.create(stone=stone, name=x,
                                             slug=slugify(x))
                    print('+', end='', flush=True)

            if stone.slug != stone.urlname:
                urlname_changes.append(
                    'Stone {} urlname changed "{}" --> "{}"'.format(
                        stone.id, stone.urlname, stone.slug))

        print('done. Some urlnames changed:\n', urlname_changes)

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

    def import_tradeshow(self):
        print('Import tradeshows', end='', flush=True)
        Tradeshow.objects.all().delete()
        for row in self.walkjsondata('tradeshows2'):
            tradeshow = Tradeshow()
            tradeshow.aumaid = row['aumaid']
            tradeshow.name = row['name'][:60]
            tradeshow.aka = row['aka'][:255]
            tradeshow.url = slugify(row['name'])[:60]
            tradeshow.city_name = row['city'][:60]
            tradeshow.country_name = row['country'][:60]
            tradeshow.begins = parse_iso_date(row['begins'])
            tradeshow.ends = parse_iso_date(row['ends'])
            tradeshow.keywords = row['keywords']
            tradeshow.about = row['about']
            tradeshow.web = row['web'][:250]
            tradeshow.contact = row['contact'][:250]
            tradeshow.logo = row['logo'][:60]
            tradeshow.save()
            print('.', end='', flush=True)
        print(' done')

    def import_group(self):
        """
        {"id":"15","topic_id":"0","name":"Stone Installation","url":"stone-installer","about":"Natural stone companies specialized in the installtion of granite, marble and similar natural stones. Installation of natural stone as flooring, wall cladding, counter tops or as other application.","description":"Companies specialized in the installtion of granite, marble and related natural stones, as flooring, wall cladding, counter tops or other applications.","keywords":"installation of stone, granite, marble, limestone, flooring, wall cladding","title_foto":"305","title_foto_ext":"jpg","count_members":"554","created_time":"2007-10-27 23:12:54","created_ip":"127.0.0.1","created_user":"1","time":"2008-08-18 06:27:47","ip":"84.137.125.24","is_invite_only":"0","is_private":"0","is_blocked":"0","is_deleted":"0"},
        """
        print('Import groups: ', end='', flush=True)
        Group.objects.all().delete()
        for row in self.walkjsondata('groups'):
            group = Group(id=row['id'])
            group.name = row['name'][:30]
            group.slug = row['url'][:30]  # url
            group.about = row['about']
            group.description = row['description'][:255]
            group.keywords = row['keywords'][:255]
            group.title_foto = '/static/group/{}.jpg'.format(group.slug)
            group.count_members = row['count_members']
            group.created = parse_iso_datetime(row['created_time'])
            group.save()
            print('g', end='', flush=True)
            # add members of this group
            """
            {"user_id":"4","group_id":"13","applied_time":"2008-08-17 04:40:27","confirmed_time":"2008-08-17 04:40:27"}
            """
            for row2 in self.walkjsondata('groups_members'):
                if row2['group_id'] == group.id:
                    try:
                        user = User.objects.get(pk=row2['user_id'])
                        group.members.add(user)
                        print('.', end='', flush=True)
                    except User.DoesNotExist:
                        # print('Could not add user {} to group {}: User does '
                        #      'not exist.'.format(row2['user_id'], group.name))
                        print('X', end='', flush=True)
        print('all groups done')

    def import_profile(self):
        # Does NOT delete user profiles but simply overwrites values in
        # existing ones that were created by import_user previously.
        """
        --- profile -----------------------------------------------------------
        {"user_id":"1","nick":"admin","name":"Graniteland","contact":
        "xxxxxxx","contact_position":"","slogan":"","street":"","city":"",
        "zip":"","country_sub_id":"0","country_id":"0","country_sub_name":"",
        "country_name":"","postal":"","email":"info@graniteland.com","fax":"",
        "tel":"","mobile":"","web":"","about":"","title_foto":"0",
        "title_foto_ext":""}
        """
        i = 0
        count = User.objects.all().count()
        print('Update user profiles for {} users.'.format(count))

        for row in self.walkjsondata('user_profiles'):
            i += 1
            pk = force_int(row['user_id'])
            try:
                profile = UserProfile.objects.get(user_id=pk)
            except UserProfile.DoesNotExist:
                print('No profile: {} {}'.format(pk, row['name']))
                continue

            print('{}/{} - Updating profile {}'
                  .format(i, count, row['name']), end=' ')

            # Figure out the country
            country_id = force_int(row['country_id'])
            country = Companydb_Country.objects.filter(pk=country_id).first()
            if country:
                print(' country {}'.format(country.name), end=' ')
                profile.country = country
            else:
                print(' no country!'.format(profile.name), end=' ')

            profile.contact = row['contact']
            profile.contact_position = row['contact_position']
            profile.slogan = row['slogan']
            profile.street = row['street']
            profile.city = row['city']
            profile.zip = row['zip']
            profile.country_sub_id = row['country_sub_id']
            profile.country_sub_name = row['country_sub_name']
            profile.country_name = row['country_name']
            profile.postal = row['postal']
            profile.email = row['email']
            profile.fax = row['fax']
            profile.tel = row['tel']
            profile.mobile = row['mobile']
            profile.web = row['web']
            profile.about = row['about']
            profile.save()
            print('.', end='', flush=True)
            print(' done!')

    def import_pics(self):
        """
        {"id":"1","user_id":"4","module":"profile","module_id":"4","folder":"0","time":"2005-06-12 08:48:06","ip":"0.0.0.0","size":"26860","width":"397","height":"297","ext":"jpg","title":"","caption":"","is_blocked":"0","is_deleted":"0","is_sticky":"0","is_comments":"0","is_approved":"1","is_title":"0"},

        companydb.modules.Pic.MODULE_CHOICES = (
            ('profile', 'Profile'), ('projects', 'Projects'),
            ('stones', 'Stones'), ('stock', 'Stock'), ('groups', 'Groups'),
            ('pages', 'Pages'))

        {'groups': 17, 'stock': 11754, 'stones': 2450,
         'projects': 1770, 'pages': 29, 'profile': 11006}
        """
        """
        print('Count pic modules:')
        m = dict()
        for row in self.walkjsondata('fotos'):
            if row['module'] in m.keys():
                m[row['module']] += 1
            else:
                m[row['module']] = 0
        print('done counting:')
        print(m)
        input('Press ENTER to continue with pics import...')
        """
        print('Import pics', end='', flush=True)
        Pic.objects.all().delete()
        i = 0
        for row in self.walkjsondata('fotos'):
            try:
                user = User.objects.get(pk=row['user_id'])
            except User.DoesNotExist:
                print('U', end='', flush=True)
                continue
            pic = Pic(id=row['id'])
            pic.user = user
            # check integrity: find the object in the referenced model
            pic.module = row['module']  # related model
            pic.module_id = row['module_id']  # object id within related model

            if pic.module == 'profile':
                try:
                    User.objects.get(pk=pic.module_id)
                except UserProfile.DoesNotExist:
                    print('U', end='', flush=True)
                    continue  # user not found!
            elif pic.module == 'projects':
                try:
                    Project.objects.get(pk=pic.module_id)
                except Project.DoesNotExist:
                    print('P', end='', flush=True)
                    continue  # project item not found!
            elif pic.module == 'stock':
                try:
                    Stock.objects.get(pk=pic.module_id)
                except Stock.DoesNotExist:
                    print('K', end='', flush=True)
                    continue  # stock item not found!
            elif pic.module == 'stones':
                try:
                    Stone.objects.get(pk=pic.module_id)
                except Stone.DoesNotExist:
                    print('S', end='', flush=True)
                    continue  # stone item not found!
            elif pic.module == 'pages':
                try:
                    Article.objects.get(pk=pic.module_id)
                except Article.DoesNotExist:
                    print('A', end='', flush=True)
                    continue  # article item not found!
            elif pic.module == 'groups':
                try:
                    Group.objects.get(pk=pic.module_id)
                except Group.DoesNotExist:
                    print('G', end='', flush=True)
                    continue  # group item not found!
            else:
                continue  # not a valid module

            pic.created = parse_iso_datetime(row['time'])
            if not pic.created:  # skip if no timestamp
                continue
            pic.size = force_int(row['size'])
            pic.width = force_int(row['width'])
            pic.height = force_int(row['height'])
            pic.ext = row['ext']
            pic.title = row['title']
            pic.caption = row['caption']
            pic.is_blocked = bool(force_int(row['is_blocked']))
            pic.is_deleted = bool(force_int(row['is_deleted']))
            if pic.is_blocked or pic.is_deleted:  # skip if deleted
                continue
            pic.is_sticky = bool(force_int(row['is_sticky']))
            pic.is_comments = bool(force_int(row['is_comments']))
            pic.is_approved = bool(force_int(row['is_approved']))
            pic.is_title = bool(force_int(row['is_title']))
            pic.save()
            i += 1
            print('.', end='', flush=True)
            if (i % 1000) == 0:
                print(i, end='', flush=True)
        print('done. {} pics imported.'.format(i))

    def import_stock(self):
        i = 0
        print('Import stock', end='', flush=True)
        Stock.objects.all().delete()
        for row in self.walkjsondata('stones_stock'):
            try:
                stone = Stone.objects.get(pk=row['stone_id'])
            except Stone.DoesNotExist:
                # print('Stone not found for stock {}'.format(row['stone_id']))
                print('SE', end='', flush=True)
                continue
            try:
                user = User.objects.get(pk=row['user_id'])
            except User.DoesNotExist:
                # print('User not found for stock {}'.format(row['user_id']))
                print('UE', end='', flush=True)
                continue
            item = Stock(id=row['id'])
            item.user = user
            item.stone = stone
            item.created = parse_iso_datetime(row['time'])
            if not item.created:  # skip if no created time
                continue
            item.description = row['description']
            item.is_blocked = bool(force_int(row['is_blocked']))
            item.is_deleted = bool(force_int(row['is_deleted']))
            if item.is_blocked or item.is_deleted:  # skip deleted items
                continue
            item.is_recommended = bool(force_int(row['is_recommended']))
            item.count_views = force_int(row['count_views'])
            item.save()

            i += 1
            print('.', end='', flush=True)
            if (i % 1000) == 0:
                print(i, end='', flush=True)
        print('done. {} stock items imported.'.format(i))

    def import_projects(self):
        i = 0
        print('Import project', end='', flush=True)
        Project.objects.all().delete()
        for row in self.walkjsondata('stones_projects'):
            try:
                stone = Stone.objects.get(pk=row['stone_id'])
            except Stone.DoesNotExist:
                # print('Stone not found for proj. {}'.format(row['stone_id']))
                print('SE', end='', flush=True)
                continue
            try:
                user = User.objects.get(pk=row['user_id'])
            except User.DoesNotExist:
                # print('User not found for project {}'.format(row['user_id']))
                print('UE', end='', flush=True)
                continue
            item = Project(id=row['id'])
            item.user = user
            item.created = parse_iso_datetime(row['time'])
            if not item.created:  # skip if no created time
                continue
            item.description = row['description']
            item.is_blocked = bool(force_int(row['is_blocked']))
            item.is_deleted = bool(force_int(row['is_deleted']))
            if item.is_blocked or item.is_deleted:  # skip deleted items
                continue
            item.is_recommended = bool(force_int(row['is_recommended']))
            item.count_views = force_int(row['count_views'])
            item.save()

            item.stones.add(stone)
            item.save()

            i += 1
            print('.', end='', flush=True)
            if (i % 1000) == 0:
                print(i, end='', flush=True)
        print('done. {} project items imported.'.format(i))

    def import_pages(self):
        # pages_topics
        # pages

        Article.objects.all().delete()
        Author.objects.all().delete()
        Keyword.objects.all().delete()
        Topic.objects.all().delete()

        print('Import topics ', end='', flush=True)
        for row in self.walkjsondata('pages_topics'):
            item = Topic(id=row['id'])
            item.title = row['title']
            item.slug = row['url'][:50]
            item.description = row['description']
            item.save()
            print('.', end='', flush=True)
        print(' done!')

        print('Import authors', end='', flush=True)
        for row in self.walkjsondata('pages'):
            a = row['author_name']
            b = {'about': row['author_about'], 'url': row['author_url']}
            item, created = Author.objects.get_or_create(name=a, defaults=b)
            if created:
                print('.', end='', flush=True)
        print(' done!')

        print('Import keywords', end='', flush=True)
        for row in self.walkjsondata('pages'):
            pass
        print(' NOT IMPLEMENTED!')

        print('Import articles', end='', flush=True)
        user = User.objects.get(pk=1)
        for row in self.walkjsondata('pages'):
            item = Article(id=row['id'])
            item.title = row['title']
            item.slug = row['url'][:50]
            item.created = parse_iso_datetime(row['time'])
            item.user = user
            try:
                item.author = Author.objects.get(name=row['author_name'])
            except Author.DoesNotExist:
                item.author = None
            item.is_published = bool(int(row['is_published']))
            item.is_stickied = False
            item.is_frontpage = True
            item.topic = Topic.objects.get(pk=int(row['topic_id']))
            item.teaser = row['teaser']
            item.description = row['description']
            item.text = row['text']
            item.save()

            for k in row['keywords'].split(', '):
                kslug = slugify(k)[:50]
                if not kslug:
                    continue
                kobj, created = Keyword.objects.get_or_create(slug=kslug)
                item.keywords.add(kobj)
                print('.', end='', flush=True)

            print('.', end='', flush=True)
        print(' done!')

    def fix_all_id(self):
        # Fixed all auto_increment id values for all models. There was a problem
        # on the companydb.models.Pic model, so just fix them all to be safe.
        os.environ['DJANGO_COLORS'] = 'nocolor'
        commands = StringIO()
        cursor = connection.cursor()
        for label in ['companydb', 'stonedb', 'tradeshowdb', 'mdpages']:
            call_command('sqlsequencereset', label, stdout=commands)
            print('Will fix "{}".'.format(label))
        cursor.execute(commands.getvalue())

