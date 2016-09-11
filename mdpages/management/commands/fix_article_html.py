from django.core.management.base import BaseCommand
from companydb.models import update_company_properties
from stonedb.models import update_stone_properties


class Command(BaseCommand):
    args = ""
    help = ('Update the JSON files with search options in the page header '
            'for company, stone, and tradeshow searches.')

    def handle(self, *args, **options):
        regexes = [
            (r'<p[^>]', '\n'),
            (r'</p[^>]', '\n'),
            (r'<br[^>]', '\n'),
            (r'<strong[^>]', '<strong>'),
            (r'</strong[^>]', '</strong>'),
        ]

        for article in Article.objects.all():
            article.title = article.title.replace('<p', '')
