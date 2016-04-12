from django.core.management import BaseCommand

from companydb.models import Pic


class Command(BaseCommand):
    args = ""
    help = "Re-create uploaded media files for companydb.Pic model."

    def handle(self, *args, **options):
        count_oserror = 0
        count_notfound = 0
        count_success = 0
        li = Pic.objects.all_public()

        print('\nCreate image files for all sizes of each uploaded, public\n'
              'picture. There are currently {} items.\n'.format(li.count()))
        input('--- Press ENTER to continue ---')

        for pic in li:
            try:
                pic.make_sizes(force=True)
                print('.', end='', flush=True)
                count_success += 1
            except FileNotFoundError as e:
                print('[NF:{}]'.format(pic.id), end='', flush=True)
                count_notfound += 1
            except OSError as e:
                print('[OS:{}]'.format(pic.id), end='', flush=True)
                count_oserror += 1

        print(' done.')
        print('OS Errpr: {} -- Not Found Error: {} -- Success: {}\n'.format(
            count_oserror, count_notfound, count_success))
