import os

from os.path import join, dirname

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from mdpages.models import Article
from stonedb.models import Stone
from django.utils.timezone import now

from toolbox import resize_copy


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile', primary_key=True)
    name = models.CharField(
        max_length=100, default='',
        verbose_name=_('Company name'),
        help_text=_('The name of your company.'))
    contact = models.CharField(
        max_length=100, default='', blank=True,
        verbose_name=_('Contact person'),
        help_text=_('The name of your company.'))
    contact_position = models.CharField(
        max_length=100, default='', blank=True,
        verbose_name=_('Contact position'),
        help_text=_('The job title of the contact person (sales, owner, etc.)'))
    slogan = models.CharField(
        max_length=255, default='', blank=True,
        verbose_name=_('Company slogan'),
        help_text=_('A very short sentence thath expresses '
                    'the company focus and values.'))
    street = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('Street'),
        help_text=_('The physical address of the company.'))
    city = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('City'),
        help_text=_('The name of the city or town.'))
    zip = models.CharField(
        max_length=16, default='', blank=True, verbose_name=_('Postal code'),
        help_text=_('The postal code.'))
    country_sub_id = models.PositiveIntegerField(db_index=True, default=0)
    country_id = models.PositiveIntegerField(db_index=True, default=0)
    country_sub_name = models.CharField(
        max_length=100, default='', blank=True,
        verbose_name=_('Province/Region'),
        help_text=_('The province or region if applicable.'))
    country_name = models.CharField(
        max_length=100, default='', blank=True,
        verbose_name=_('Country name'),
        help_text=_('The country your company is registered.'))
    postal = models.TextField(default='', verbose_name=_('Postal address'))
    email = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('E-mail'),
        help_text=_('Official company sales email address.'))
    fax = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('Fax'),
        help_text=_("Your company's fax number."))
    tel = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('Phone'),
        help_text=_("Your company's phone number, including "
                    "international dialing code for your country."))
    mobile = models.CharField(
        max_length=100, default='', blank=True, verbose_name=_('Mobile phone'),
        help_text=_('Your mobile phone number.'))
    web = models.CharField(
        max_length=100, default='', blank=True,
        verbose_name=_('Company website'),
        help_text=_('The official web site of your company, if applicable.'))
    about = models.TextField(
        default='', blank=True,
        verbose_name=_('About company'),
        help_text=_('Provide some background about your company'))
    title_foto = models.IntegerField(default=0)
    title_foto_ext = models.CharField(max_length=30, default='')
    signup_ip = models.CharField(max_length=15, default='')
    lastlogin_ip = models.CharField(max_length=15, default='')
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.name

    @property
    def stock_count(self):
        return self.user.stock_set.all().count()

    @property
    def project_count(self):
        return self.user.project_set.all().count()

    @property
    def pic_count(self):
        return Pic.objects.filter(module='profile',
                                  module_id=self.user.id).count()

    @property
    def title_foto_url(self):
        if self.title_foto:
            thumb_dir = 'fotos_thumb'
            return join(settings.MEDIA_URL, thumb_dir, '{}.{}'.format(
                        self.title_foto, self.title_foto_ext))
        else:
            return ''


class CommonProjectsStocksManager(models.Manager):
    def all_for_user(self, user):
        return self.all_public().filter(user=user)


class CommonProjectsStocks(models.Model):
    user = models.ForeignKey(User, db_index=True, editable=False)
    created = models.DateTimeField(default=now, editable=False)  # time
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    count_views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        abstract = True


class StockManager(CommonProjectsStocksManager):
    def all_for_stone(self, stone):
        return self.all_public().filter(stone=stone)

    def all_public(self):
        return self.exclude(is_blocked=True, is_deleted=True)\
                   .prefetch_related('stone', 'user', 'user__profile')


class Stock(CommonProjectsStocks):
    # Dimension type: depending on this, use square or cubic centimeter.
    DIM_TYPE_CHOICES = ((0, _('not specified')),
                        (1, _('blocks')),
                        (2, _('slabs')),
                        (3, _('tiles')),
                        (4, _('cobblestone')),
                        (9, _('other')), )
    DIM_USE_CUBIC = {1, 4, }

    stone = models.ForeignKey(Stone, db_index=True, null=True, default=None)
    description = models.TextField(
        default='', blank=True, verbose_name=_('Stock item description'),
        help_text=_('Add any information about the stock item here, '
                    'i.e. sizes, surface treatment, borders, etc.'))
    dim_type = models.PositiveSmallIntegerField(
        choices=DIM_TYPE_CHOICES, default=0, blank=True,
        verbose_name=_('Product type'),
        help_text=_('Specify the product type of of your stock item.'))
    # total amount in square meters or cubic meters
    dim_total = models.PositiveIntegerField(
        default=0, blank=True, verbose_name=_('Total amount'),
        help_text=_('Total amount in square meters or cubic meters.'))

    objects = StockManager()

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ('-created', )

    def __str__(self):
        return '{} --> {}'.format(self.user.profile.name, self.stone.name)

    def get_pics_list(self):
        return Pic.objects.all_for_stock(self)

    def get_dim_unit_name(self):
        if self.dim_type in self.DIM_USE_CUBIC:
            return 'cubic meters'
        else:
            return 'square meters'

    def get_dim_unit_short(self):
        if self.dim_type in self.DIM_USE_CUBIC:
            return 'm²'
        else:
            return 'm³'


class ProjectsManager(CommonProjectsStocksManager):
    def all_for_stone(self, stone):
        """Return all projects that contain "stone" in their "stones" list."""
        return self.all_public().filter(stones=stone)

    def all_public(self):
        return self.exclude(is_blocked=True, is_deleted=True)\
                   .prefetch_related('user', 'user__profile')


class Project(CommonProjectsStocks):
    stones = models.ManyToManyField(
        Stone, null=True, default=None,
        verbose_name=_('Stones used'),
        help_text=_('Start typing the name of a stone used in the project, '
                    'then select the stones from the list. Add all stones used '
                    'in the project, but not more than ten.'))
    description = models.TextField(
        default='', blank=True,
        verbose_name=_('Project description'),
        help_text=_('Describe the project, the challenges you met, the '
                    'problems you solved, the time it took, etc.'))
    location = models.TextField(
        default='', blank=True,
        verbose_name=_('Address'),
        help_text=_('ONLY for publicly accessible buildings, provide a street'
                    'address of the project, where it can be visited.'))
    lat = models.FloatField(null=True, default=None, editable=False)
    lng = models.FloatField(null=True, default=None, editable=False)

    objects = ProjectsManager()

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ('-created', )

    def __str__(self):
        return '{}'.format(self.pk)

    def get_pics_list(self):
        return Pic.objects.all_for_project(self)

    def get_stones_list(self):
        return self.stones.all()


class PicManager(models.Manager):
    def all_public(self):
        return self.exclude(is_blocked=True, is_deleted=True)

    def all_for_user(self, user):
        return self.all_public().filter(user=user)

    def all_for_stone(self, pk):
        """Return a QuerySet with all pictures for a stone.
        :param pk: Either a stone id or a Stone instance.
        """
        if isinstance(pk, Stone):
            pk = pk.pk
        return self.all_public().filter(module='stones', module_id=pk)

    def all_for_profile(self, pk):
        """Return a QuerySet with all pictures for a user profile.
        :param pk: Either a user id or a User instance.
        """
        if isinstance(pk, User):
            pk = pk.pk
        return self.all_public().filter(module='profile', module_id=pk)

    def all_for_project(self, pk):
        """Return a QuerySet with all pictures for a project.
        :param pk: Either a project id or a Project instance.
        """
        if isinstance(pk, Project):
            pk = pk.pk
        return self.all_public().filter(module='projects', module_id=pk)

    def all_for_stock(self, pk):
        """Return a QuerySet with all pictures for a stock item.
        :param pk: Either a stock id or a Stock instance.
        """
        if isinstance(pk, Stock):
            pk = pk.pk
        return self.all_public().filter(module='stock', module_id=pk)

    def all_for_group(self, pk):
        """Return a QuerySet with all pictures for a group.
        :param pk: Either a group id or a Group instance.
        """
        if isinstance(pk, Group):
            pk = pk.pk
        return self.all_public().filter(module='groups', module_id=pk)

    def all_for_page(self, pk):
        """Return a QuerySet with all pictures for a page/article.
        :param pk: Either a article id or a mdpages.models.Article instance.
        """
        if isinstance(pk, Article):
            pk = pk.pk
        return self.all_public().filter(module='pages', module_id=pk)

    def add_upload(self, user, file, module, module_id=0, title='', caption=''):
        """
        Store an uploaded image file, create all image sizes, and then return
        the new image's Pic instance.

        :param user: The user who creates the picture.
        :param file: The uploaded file tmp name from "request.FILES".
        :param module: Module name 'profile', 'stock', 'stones', etc.
        :param module_id: The object id of the related item.
        :param title: Optional title for the picture.
        :param caption: Optional caption for the picture.
        """
        pic = Pic()
        pic.user = user
        pic.module = module
        pic.module_id = module_id
        pic.title = title
        pic.caption = caption
        pic.save()

        # Store the raw file and create all image sizes.
        with open(pic.get_filename(), 'wb+') as fh:
            for chunk in file.chunks():
                fh.write(chunk)

        pic.make_sizes()
        return pic

    def add_to_profile(self, user, file, title='', caption=''):
        """Shortcut method to upload a picture to a user profile.
        :param user: A user instance. Picture is added to this user's profile.
        :param file: A single picture file object from "request.FILES".
        :param title: Optionally, a title string.
        :param caption: Optionally, a caption string.
        """
        return self.add_upload(user, file, 'profile', user.id, title, caption)


class Pic(models.Model):  # cc__fotos
    """All user uploaded pictures for profiles, projects, stock items, etc"""

    MODULE_CHOICES = (
        ('profile', 'Profile'), ('projects', 'Projects'), ('stones', 'Stones'),
        ('stock', 'Stock'), ('groups', 'Groups'), ('pages', 'Pages'))

    RAW = 'fotos_raw'

    # WATERMARK = join(settings.BASE_DIR,
    #                  'gl4app', 'static', 'img', 'watermark.gif')
    WATERMARK = True

    SIZES = (  # size_name, resize_type, max_width, max_height, watermark
        ('fotos_large', 'contain', 1024, 800, WATERMARK),
        ('fotos_medium', 'contain', 640, 480, WATERMARK),
        ('fotos_small', 'contain', 480, 200, None),
        ('fotos_thumb', 'cover', 200, 200, None), )

    user = models.ForeignKey(User, db_index=True)
    module = models.CharField(max_length=20,
                              choices=MODULE_CHOICES, default='profile')
    module_id = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=now)  # time
    size = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    ext = models.CharField(max_length=3, default='jpg')
    title = models.CharField(max_length=80, default='', blank=True,
                             help_text='A short title for the picture.')
    caption = models.TextField(default='', blank=True, help_text='Optionally, '
                               'some more information about the picture.')
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)
    is_comments = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_title = models.BooleanField(default=False)

    objects = PicManager()

    class Meta:
        verbose_name = "Picture"
        verbose_name_plural = "Pictures"
        ordering = ('-created', )

    def __str__(self):
        return '{}.{}'.format(self.id, self.ext)

    @property
    def url_thumb(self):
        return self.get_url('fotos_thumb')

    @property
    def url_small(self):
        return self.get_url('fotos_small')

    @property
    def url_medium(self):
        return self.get_url('fotos_medium')

    @property
    def url_large(self):
        return self.get_url('fotos_large')

    def get_url(self, size):
        if size == 'raw':
            raise ValueError('Raw image files are not accessible')

        return join(settings.MEDIA_URL, size, '{}.{}'.format(self.id, 'jpg'))

    def get_filename(self, size=None):
        ext = 'jpg'  # all sizes will be JPEG.
        if not size:
            size = Pic.RAW
            ext = self.ext  # use extention of uploaded file.
        elif size not in [x[0] for x in Pic.SIZES]:
            raise ValueError('Not a define image size, see Pic.SIZES')

        return join(settings.MEDIA_ROOT, size, '{}.{}'.format(self.id, ext))

    def make_sizes(self):
        """Creates all image file sizes Pic.models.SIZE for this instance."""
        raw_fname = self.get_filename()

        for x in Pic.SIZES:
            size_name, resize_type, max_width, max_height, watermark = x
            fname = self.get_filename(size_name)
            # Make sure the directory exists
            os.makedirs(dirname(fname), mode=0o755, exist_ok=True)
            # Try to delete any old thumb image file
            try:
                os.remove(fname)
            except OSError:
                pass
            resize_copy(raw_fname, fname, resize_type,
                        max_width, max_height, watermark)
            os.chmod(fname, 0o644)

        return True

    def delete_file(self, size):
        """Delete the image file for size 'size'.
        :param size: Size name.
        """
        try:
            os.remove(self.get_filename(size))
        except OSError:
            pass

        return None

    def delete_all_files(self):
        """Deletes all files of the current Pic instance, including RAW.
        :rtype: None
        """
        for size in Pic.SIZES:
            self.delete_file(size[0])
        try:
            os.remove(self.get_filename())
        except OSError:
            pass

        return None

    def attach_to(self, module_id, module=None):
        """
        Attach the instance to a specific object of a module, and commit it.
        If no module name is provided, the instance's existing module name
        is used.

        :param module_id: the pk of an object in the instances attached module.
        :param module: optional module identifier string.
        :return:
        """
        if module:
            self.module = module
        else:
            pass  # self.module is already set correctly.

        if self.module not in [x[0] for x in Pic.MODULE_CHOICES]:
            raise ValueError('"{}" is not a valid module choice'.format(module))

        self.module_id = module_id
        self.save()


class Group(models.Model):
    name = models.CharField(max_length=30, default='')
    slug = models.CharField(max_length=30, default='')  # url
    about = models.TextField(default='')  # intro text for group page
    description = models.CharField(max_length=255, default='')
    keywords = models.CharField(max_length=255, default='')
    title_foto = models.ForeignKey(Pic, null=True, default=None)
    count_members = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(default=now)  # created_time
    members = models.ManyToManyField(User)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ('name', )

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_profile_on_user_create(sender, instance=None,
                                  created=False, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(pre_delete, sender=Pic)
def delete_related_files_on_pic_delete(sender, instance, using, **kwargs):
    instance.delete_all_files()
