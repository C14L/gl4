from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from stonedb.models import Stone
from django.utils.timezone import now


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


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

    def all_for_stone(self, stone):
        return self.all_public().filter(module='stones', module_id=stone.id)

    def all_for_profile(self, user):
        return self.all_public().filter(module='profile', module_id=user.id)

    def all_for_project(self, project):
        return self.all_public().filter(module='projects', module_id=project.id)

    def all_for_stock(self, stock):
        return self.all_public().filter(module='stock', module_id=stock.id)

    def all_for_group(self, group):
        return self.all_public().filter(module='groups', module_id=group.id)

    def all_for_page(self, page):
        return self.all_public().filter(module='pages', module_id=page.id)


class Pic(models.Model):  # cc__fotos
    """All user uploaded pictures for profiles, projects, stock items, etc"""

    MODULE_CHOICES = (
        ('profile', 'Profile'), ('projects', 'Projects'), ('stones', 'Stones'),
        ('stock', 'Stock'), ('groups', 'Groups'), ('pages', 'Pages'))

    user = models.ForeignKey(User, db_index=True)
    module = models.CharField(max_length=20,
                              choices=MODULE_CHOICES, default='profile')
    module_id = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=now)  # time
    size = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    ext = models.CharField(max_length=3, default='jpg')
    title = models.CharField(max_length=80, default='')
    caption = models.TextField(default='')
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

    def __str__(self):
        return '{}.{}'.format(self.id, self.ext)

    @property
    def url_small(self):
        return settings.PIC_SMALL_URL + '{}.{}'.format(self.id, self.ext)

    @property
    def url_medium(self):
        return settings.PIC_MEDIUM_URL + '{}.{}'.format(self.id, self.ext)

    @property
    def url_large(self):
        return settings.PIC_LARGE_URL + '{}.{}'.format(self.id, self.ext)


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
