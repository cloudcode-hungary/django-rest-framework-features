import re

from django.core.management.base import BaseCommand, CommandError

from rest_framework_features import schema


class Command(BaseCommand):
    help = 'CLI utility for django-rest-framework-features'

    def add_arguments(self, parser):
        self.parser = parser
        parser.add_argument(
            '--json',
            action='store_true',
            default=False,
            help='Use this flag to print the json schema to stdout',
        )
        parser.add_argument(
            '--locale-js',
            action='store_true',
            default=False,
            help='Use this flag to print the js api locale to stdout',
        )
        parser.add_argument(
            '--locale-py',
            action='store_true',
            default=False,
            help='Use this flag to print the python api locale to stdout',
        )

    def handle(self, *args, **options):
        if options['json']:
            self.stdout.write(re.sub(r'\s+', '', schema.render_json_schema()))
        elif options['locale_js']:
            self.stdout.write(schema.render_locale_js_schema())
        elif options['locale_py']:
            self.stdout.write(schema.render_locale_py_schema())
        else:
            self.parser.print_help()
            raise CommandError('no options provided')
