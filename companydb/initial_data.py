"""
Provide functions to import initial data that is not formated to be handled by
Django's standard fixture importer.
"""
import csv

from django.conf import settings
from os.path import join

from companydb.models import Country
from toolbox import force_int


def import_company_countries(force=False, silent=False):
    if force:
        Country.objects.all().delete()

    header = ['iso', 'iso3', 'iso_numeric', 'fips', 'country', 'capital',
              'area', 'population', 'continent', 'tld', 'currency_code',
              'currency_name', 'phone', 'postal_code_format',
              'postal_code_regex', 'languages', 'geonameid', 'neighbours',
              'equivalent_fips_code']
    filename = 'countryInfo_{}.txt'.format(settings.LANGUAGE_SHORT)
    filename = join(settings.BASE_DIR, '..', 'fixtures', filename)

    with open(filename, newline='') as fh:
        reader = csv.DictReader(filter(lambda row: row[0] != '#', fh),
                                fieldnames=header, delimiter='\t',
                                quoting=csv.QUOTE_NONE, lineterminator='\n')

        for raw in reader:
            pk = force_int(raw['iso_numeric'])
            geonameid = force_int(raw['geonameid'])
            if raw['country'] == 'Democratic Republic of the Congo':
                raw['country'] = 'D.R.Congo'
            if raw['country'] == 'United States':
                raw['country'] = 'U.S.A.'

            if int(raw['population']) < 50000:
                continue
            if not (geonameid and pk):
                continue
            if raw['country'] in (
                    'Saint Vincent and the Grenadines', 'Reunion',
                    'Netherlands Antilles', 'Isle of Man',
                    'Serbia and Montenegro', 'U.S. Virgin Islands',
                    'Northern Mariana Islands', 'Jersey', ):
                continue
            if Country.objects.filter(pk=pk).first():
                continue

            if not silent:
                print('{}'.format(raw['iso']), end=' ', flush=True)

            Country.objects.create(
                id=pk, name=raw['country'], geonameid=geonameid,
                cc=raw['iso'][:2], phone=raw['phone'][:10])

    if not silent:
        print('ok.')
