from django.core.management.base import BaseCommand, CommandError


class _Base(BaseCommand):
    @staticmethod
    def _validate_options(options):
        if options['json']:
            return
        if not options['app']:
            raise CommandError('Option "app" is required')
        if not options['model']:
            raise CommandError('Option "model" is required')
        if not options['field']:
            raise CommandError('Option "field" is required')

    @staticmethod
    def _get_data(fields):
        data = dict()
        for field in fields:
            try:
                key, value = field.split('=')
            except ValueError:
                raise CommandError('Invalid field format (e.g., field=value)')

            data[key] = value

        return data

    def add_arguments(self, parser):
        parser.add_argument('--json', '-j', type=str)
        parser.add_argument('--app', '-a', type=str)
        parser.add_argument('--model', '-m', type=str)
        parser.add_argument('--field', '-f', type=str, action='append', help="Field to add/update")

    def handle(self, *args, **options):
        raise NotImplemented
