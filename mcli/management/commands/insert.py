from django.core.management import CommandError
from django.db import IntegrityError
from getter import get_model

from mcli.management.commands._base import _Base


class Command(_Base):
    help = 'Create an object of a model and save it into database'

    def handle(self, *args, **options):
        self._validate_options(options)
        data = self._get_data(options['field'])
        self.stdout.write(self.style.MIGRATE_HEADING('Inserting record:'))

        model = get_model(app_label=options['app'], model=options['model'])
        try:
            self.stdout.write(self.style.MIGRATE_LABEL(f"  Inserting into {options['model']} ({data})... "), ending='')
            obj = model.objects.create(**data)
            obj.save()
            self.stdout.write(self.style.SUCCESS('OK'))
        except IntegrityError as e:
            raise CommandError(f'Integrity error ({str(e)})')
