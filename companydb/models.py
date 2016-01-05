import os

from os.path import join

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from mdpages.models import Article
from stonedb.models import Stone
from django.utils.timezone import now

from toolbox import resize_copy


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile', primary_key=True)
    name = models.CharField(max_length=100, default='')
    contact = models.CharField(max_length=100, default='')
    contact_position = models.CharField(max_length=100, default='')
    slogan = models.CharField(max_length=255, default='')
    street = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    zip = models.CharField(max_length=16, default='')
    country_sub_id = models.PositiveIntegerField(db_index=True, default=0)
    country_id = models.PositiveIntegerField(db_index=True, default=0)
    country_sub_name = models.CharField(max_length=100, default='')
    country_name = models.CharField(max_length=100, default='')
    postal = models.TextField(default='')
    email = models.CharField(max_length=100, default='')
    fax = models.CharField(max_length=100, default='')
    tel = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=100, default='')
    web = models.CharField(max_length=100, default='')
    about = models.TextField(default='')
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
            return '{}{}.{}'.format(settings.PIC_SMALL_URL,
                                    self.title_foto, self.title_foto_ext)
        else:
            return ''


class CommonProjectsStocksManager(models.Manager):

    def all_public(self):
        return self.exclude(is_blocked=True, is_deleted=True)\
                   .prefetch_related('stone', 'user', 'user__profile')

    def all_for_stone(self, stone):
        return self.all_public().filter(stone=stone)

    def all_for_user(self, user):
        return self.all_public().filter(user=user)


class CommonProjectsStocks(models.Model):

    stone = models.ForeignKey(Stone, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    created = models.DateTimeField(default=now)  # time
    description = models.TextField(default='')
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    count_views = models.PositiveIntegerField(default=0)

    objects = CommonProjectsStocksManager()

    class Meta:
        abstract = True

    def __str__(self):
        return '{} --> {}'.format(self.user.profile.name, self.stone.name)


class Stock(CommonProjectsStocks):

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ('-created', )

    def get_pics_list(self):
        return Pic.objects.all_for_stock(self)


class Project(CommonProjectsStocks):

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ('-created', )

    def get_pics_list(self):
        return Pic.objects.all_for_project(self)


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

    def add_upload(self, user, file, module, module_id, title='', caption=''):
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
    title = models.CharField(max_length=80, default='', blank=True)
    caption = models.TextField(default='', blank=True)
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
        if not size:
            size = Pic.RAW
        elif size not in [x[0] for x in Pic.SIZES]:
            raise ValueError('Not a define image size, see Pic.SIZES')

        return join(settings.MEDIA_ROOT, size, '{}.{}'.format(self.id, 'jpg'))

    def make_sizes(self):
        """Creates all image file sizes Pic.models.SIZE for this instance."""
        raw_fname = self.get_filename()

        for x in Pic.SIZES:
            size_name, resize_type, max_width, max_height, watermark = x
            fname = self.get_filename(size_name)
            # Try to delete any old thumb image file
            try:
                os.remove(fname)
            except OSError:
                pass
            resize_copy(raw_fname, fname, resize_type,
                        max_width, max_height, watermark)
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
