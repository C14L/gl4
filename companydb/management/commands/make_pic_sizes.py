from django.core.management import BaseCommand

from companydb.models import Pic


class Command(BaseCommand):
    args = ""
    help = "Re-create uploaded media files for companydb.Pic model."

    def handle(self, *args, **options):
        for pic in Pic.objects.all_public():
            pic.make_sizes()
