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
            self.print_json()
        elif options['locale_js']:
            self.print_locale_js_schema()
        elif options['locale_py']:
            self.print_locale_py_schema()
        else:
            self.parser.print_help()
            raise CommandError('no options provided')

    def print_json(self):
        json_schema = schema.get_schema_template('feature_schema.json')
        self.stdout.write(re.sub(r'\s+', '', json_schema))

    def print_locale_js_schema(self):
        locale_schema = schema.get_schema_template('feature_locale.js')
        self.stdout.write(locale_schema)

    def print_locale_py_schema(self):
        locale_schema = schema.get_schema_template('feature_locale.py')
        self.stdout.write(locale_schema)
