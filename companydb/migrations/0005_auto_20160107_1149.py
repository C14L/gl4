# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0003_auto_20151231_1550'),
        ('companydb', '0004_auto_20160105_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='stone',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='stone',
        ),
        migrations.AddField(
            model_name='project',
            name='stones',
            field=models.ManyToManyField(to='stonedb.Stone'),
        ),
        migrations.AddField(
            model_name='stock',
            name='stones',
            field=models.ManyToManyField(to='stonedb.Stone'),
        ),
        migrations.AlterField(
            model_name='pic',
            name='caption',
            field=models.TextField(help_text='Optionally, some more information about the picture.', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='pic',
            name='title',
            field=models.CharField(max_length=80, help_text='A short title for the picture.', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(help_text='Provide some background about your company', verbose_name='About company', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=100, help_text='The name of the city or town.', verbose_name='City', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='contact',
            field=models.CharField(max_length=100, help_text='The name of your company.', verbose_name='Contact person', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='contact_position',
            field=models.CharField(max_length=100, help_text='The job title of the contact person (sales, owner, etc.)', verbose_name='Contact position', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country_name',
            field=models.CharField(max_length=100, help_text='The country your company is registered.', verbose_name='Country name', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country_sub_name',
            field=models.CharField(max_length=100, help_text='The province or region if applicable.', verbose_name='Province/Region', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(max_length=100, help_text='Official company sales email address.', verbose_name='E-mail', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='fax',
            field=models.CharField(max_length=100, help_text="Your company's fax number.", verbose_name='Fax', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(max_length=100, help_text='Your mobile phone number.', verbose_name='Mobile phone', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=100, help_text='The name of your company.', verbose_name='Company name', default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='postal',
            field=models.TextField(verbose_name='Postal address', default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='slogan',
            field=models.CharField(max_length=255, help_text='A very short sentence thath expressesthe company focus and values.', verbose_name='Company slogan', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='street',
            field=models.CharField(max_length=100, help_text='The physical address of the company.', verbose_name='Street', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tel',
            field=models.CharField(max_length=100, help_text="Your company's phone number, including international dialing code for your country.", verbose_name='Phone', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='web',
            field=models.CharField(max_length=100, help_text='The official web site of your company, if applicable.', verbose_name='Company website', default='', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='zip',
            field=models.CharField(max_length=16, help_text='The postal code.', verbose_name='Postal code', default='', blank=True),
        ),
    ]
