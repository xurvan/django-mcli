import json

from django.core.management import CommandError
from django.db import IntegrityError

from getter import get_model
from mcli.management.commands._base import _Base


class Command(_Base):
    help = 'Create an object of a model and save it into database'

    def _insert(self, app: str, model_name: str, data: dict):
        model = get_model(app_label=app, model=model_name)
        try:
            self.stdout.write(self.style.MIGRATE_LABEL(f'  Inserting into "{model_name}" ({data})... '), ending='')

            relations = {}
            for key, val in dict(data).items():
                if isinstance(val, list):
                    relations[key] = data.pop(key)

            obj = model.objects.create(**data)
            for key, val in relations.items():
                attr = getattr(obj, key)
                for i in val:
                    attr.add(i)

            obj.save()
            self.stdout.write(self.style.SUCCESS('OK'))
        except IntegrityError as e:
            raise CommandError(f'Integrity error ({str(e)})')

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Inserting record:'))

        if options['json']:
            with open(options['json']) as f:
                data = json.load(f)

            for app_name, app in data.items():
                for model_name, model in app.items():
                    for record in model:
                        self._insert(app_name, model_name, record)

            return

        self._validate_options(options)
        data = self._get_data(options['field'])
        self._insert(options['app'], options['model'], data)
