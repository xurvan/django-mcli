from django.contrib.contenttypes.models import ContentType
from django.core.management import CommandError
from django.db import IntegrityError

from mcli.management.commands._base import _Base


class Command(_Base):
    help = 'Create an object of a model and save it into database'

    def handle(self, *args, **options):
        self._validate_options(options)
        data = self._get_data(options['field'])

        user_type = ContentType.objects.get(app_label=options['app'], model=options['model'])
        model = user_type.model_class()
        try:
            obj = model.objects.create(**data)
            obj.save()
        except IntegrityError as e:
            raise CommandError(f'Integrity error ({str(e)})')

        self.stdout.write(self.style.SUCCESS(
            f"Record added to database (app={options['app']}, model={options['model']}, data={data})"))
