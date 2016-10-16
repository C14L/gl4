from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import get_language

from companydb.models import Spam
from stonedb.models import Stone


# noinspection PyPep8Naming
def setUpModule():
    pass
    if Stone.objects.all().count() < 1:
        from gl4app.management.commands.import_from_json import Command
        command = Command()
        command.import_color()
        command.import_classification()
        command.import_country()
        command.init_texture()  # only deletes current entries
        command.import_stone()
    Spam.objects.get_or_create(match="spam word")


# noinspection PyPep8Naming
def tearDownModule():
    pass


class StonedbTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_standard_object_urls_accessible(self):
        """Check that we get HTT200 for all paths that are supposed to exist
        for the active language."""
        lang = get_language()
        paths = []
        base = reverse('home')

        if lang == 'de':
            paths += [
                'naturstein',
                'naturstein/farbe',
                'naturstein/herkunftsland',
                'naturstein/steinart',
                'naturstein/textur',
                'naturstein/herkunftsland/deutschland',
                'naturstein/farbe/gruen',
                'naturstein/farbe/weiss/2',
                'naturstein/textur/feinkoernig',
                'naturstein/steinart/marmor',
                'naturstein/all/all/weiss/marmor',
                'naturstein/italien/all/weiss/marmor',
                'naturstein/italien/geaedert/weiss/marmor',
                'naturstein/china/feinkoernig/all/granit',
                'naturstein/china/feinkoernig/all/all',
                'naturstein/verde-argento',
                'naturstein/african-lilac',
                'naturstein/branco-ipanema',
                'naturstein/abtswinder-sandstein-grun',
                'naturstein/anrochter-stein',
            ]
        else:
            paths += [
                'stone',
                'stone/color',
                'stone/country',
                'stone/type',
                'stone/texture',
                'stone/color/yellow',
                'stone/country/germany',
                'stone/country/bosnia-and-herzegovina',
                'stone/type/marble',
                'stone/texture/coarse-grained',
                'stone/all/all/green/granite',
                'stone/china/all/green/granite',
                'stone/china/medium-grained/green/granite',
                'stone/australia/medium-grained/all/granite',
                'stone/australia/medium-grained/all/all',
                'stone/post-green-g-5128',
                'stone/balmoral-green',
                'stone/calacatta-vagli-rosato',
                'stone/arabescato-arni-classico',
            ]

        for path in paths:
            url = base + path
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, msg=url)
            self.assertContains(res, 'id="tpl-wrap"', msg_prefix=url)
