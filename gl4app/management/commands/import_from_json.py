import json
from os import rename
from os.path import join, isfile, dirname
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils.text import slugify
from companydb.models import (UserProfile, Stock, Project, Pic, Group)
from stonedb.models import (Stone, StoneName,
                            Color, Classification, Texture, Country)
from tradeshowdb.models import Tradeshow
from toolbox import parse_iso_date, parse_iso_datetime, force_int


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

        #self.import_color()
        #self.import_classification()
        #self.import_country()
        #self.init_texture()  # only deletes current entries
        #self.import_user()
        #self.import_profile()
        #self.import_stone()
        #self.import_tradeshow()
        #self.import_group()
        #self.import_stock()
        #self.import_projects()
        self.import_pics()

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

    def init_texture(self):
        Texture.objects.all().delete()

    def fetch_or_create_texture(self, texture_name):
        # return texture name and id
        texture_name = texture_name.lower().strip()
        if texture_name in ['', 'n/a', 'na']:
            return None

        item, created = Texture.objects.get_or_create(name=texture_name)
        if created:
            item.slug = slugify(item.name)
            item.save()
            print('texture --> added: {} {} -> {}'.format(
                item.id, item.slug, item.name))

        return item

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
        """
        User.objects.all().delete()
        UserProfile.objects.all().delete()
        for row in self.walkjsondata('user'):
            if row['nick'] == '':  # skip if no username
                continue
            if row['type'] != 'company':  # only allow "company" as members
                continue
            # if row['is_deleted'] or row['is_blocked']:
            #    continue

            print('user --> adding {} [{}] --> {}'.format(
                row['nick'], row['user_id'], row['name']))

            try:
                user = User(id=row['user_id'])
                user.username = row['nick'][:30]
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
            profile.save()

            print('--> User added: {} {}'.format(user.id, user.username))
        print('All users created, now update all profiles')


    def import_stone(self):
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

    def import_tradeshow(self):
        Tradeshow.objects.all().delete()
        print('--> Importing tradeshows: ', end='', flush=True)
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
        Group.objects.all().delete()
        print('--> Importing user groups: ', end='', flush=True)
        for row in self.walkjsondata('groups'):
            group = Group(id=row['id'])
            group.name = row['name'][:30]
            group.slug = row['url'][:30]  # url
            group.about = row['about']
            group.description = row['description'][:255]
            group.keywords = row['keywords'][:255]
            group.title_foto = None
            group.count_members = row['count_members']
            group.created = parse_iso_datetime(row['created_time'])
            group.save()
            print('Created group "{}", adding members '.format(group.name))
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
                        print('Could not add user {} to group {}: User does '
                              'not exist.'.format(row2['user_id'], group.name))
            print(' done')
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
        i = 0;
        for row in self.walkjsondata('user_profiles'):
            i += 1
            try:
                profile = UserProfile.objects.get(user_id=row['user_id'])
            except UserProfile.DoesNotExist:
                print('!!! No profile foudn for user {} ({})'.format(
                      row['user_id'], row['nick']))

            print('{}.-- profile --> updating {}'.format(i, row['user_id']))

            profile.contact = row['contact']
            profile.contact_position = row['contact_position']
            profile.slogan = row['slogan']
            profile.street = row['street']
            profile.city = row['city']
            profile.zip = row['zip']
            profile.country_sub_id = row['country_sub_id']
            profile.country_id = row['country_id']
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

        print('All profiles updated, done')

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
        Pic.objects.all().delete()
        print('Pics importieren', end='', flush=True)
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
                    obj = User.objects.get(pk=pic.module_id)
                except UserProfile.DoesNotExist:
                    print('UP', end='', flush=True)
                    continue  # user not found!
            elif pic.module == 'projects':
                try:
                    obj = Project.objects.get(pk=pic.module_id)
                except Project.DoesNotExist:
                    print('P', end='', flush=True)
                    continue  # project item not found!
            elif pic.module == 'stock':
                try:
                    obj = Stock.objects.get(pk=pic.module_id)
                except Stock.DoesNotExist:
                    print('K', end='', flush=True)
                    continue  # stock item not found!
            elif pic.module == 'stones':
                try:
                    obj = Stone.objects.get(pk=pic.module_id)
                except Stone.DoesNotExist:
                    print('S', end='', flush=True)
                    continue  # stone item not found!
            elif pic.module == 'pages':
                pass
            elif pic.module == 'groups':
                pass

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
        Stock.objects.all().delete()
        print('Importing stock items', end='', flush=True)
        for row in self.walkjsondata('stones_stock'):
            try:
                stone = Stone.objects.get(pk=row['stone_id'])
            except Stone.DoesNotExist:
                print('Stone not found for stock {}'.format(row['stone_id']))
                continue
            try:
                user = User.objects.get(pk=row['user_id'])
            except User.DoesNotExist:
                print('User not found for stock {}'.format(row['user_id']))
                continue
            item = Stock(id=row['id'])
            item.stone = stone
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
            i += 1
            print('.', end='', flush=True)
            if (i % 1000) == 0:
                print(i, end='', flush=True)
        print('done. {} stock items imported.'.format(i))


    def import_projects(self):
        i = 0
        Project.objects.all().delete()
        print('Importing project items', end='', flush=True)
        for row in self.walkjsondata('stones_projects'):
            try:
                stone = Stone.objects.get(pk=row['stone_id'])
            except Stone.DoesNotExist:
                print('Stone not found for project {}'.format(row['stone_id']))
                continue
            try:
                user = User.objects.get(pk=row['user_id'])
            except User.DoesNotExist:
                print('User not found for project {}'.format(row['user_id']))
                continue
            item = Project(id=row['id'])
            item.stone = stone
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
            i += 1
            print('.', end='', flush=True)
            if (i % 1000) == 0:
                print(i, end='', flush=True)
        print('done. {} project items imported.'.format(i))
