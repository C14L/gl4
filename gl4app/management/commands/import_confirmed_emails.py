from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    args = ""
    help = "For all imported users, add the confirmed email address in allauth."

    LANGUAGE = settings.LANGUAGE_SHORT

    def handle(self, *args, **options):
        print('For all imported users, add confirmed email address in allauth.')

        users = User.objects.exclude(email='')
        print('Found {} users.'.format(len(users)))

        print('Removing all current email addresses from allauth.')
        input('--- PRESS ENTER TO CONFIRM ---')
        EmailAddress.objects.all().delete()
        print('Allauth EmailAddress table cleared.')

        print('Beginning import.')
        for user in users:
            try:
                email_address = EmailAddress.objects.get(
                    user=user, email__iexact=user.email)
                print('Duplicate: {}'.format(user.email), end='', flush=True)
            except EmailAddress.DoesNotExist:
                email_address = EmailAddress.objects.create(
                    user=user, email=user.email, verified=True, primary=True)
                print('.', end='', flush=True)
        print('')
        print('Import done.')
