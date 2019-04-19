from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a new app based on the smartfactory template'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, name, **options):
        options['template'] = 'template_support/app_template'
        management.call_command('startapp', name, **options)
