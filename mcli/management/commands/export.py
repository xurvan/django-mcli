import json
from django.apps import apps
from django.core.management import CommandError
from django.db import IntegrityError

from getter import get_model
from mcli.management.commands._base import _Base


class Command(_Base):
    help = 'Create an object of a model and save it into database'

    def handle(self, *args, **options):
        data = dict()
        for app in apps.all_models:
            if not apps.all_models[app]:
                continue

            data[app] = {}
            for model in apps.all_models[app]:
                model_class = get_model(model, app)
                rows = model_class.objects.all()

                data[app][model] = []
                for row in rows:
                    record = dict()
                    for k, v in row.__dict__.items():
                        if k.startswith('_'):
                            continue
                        record[k] = v

                    data[app][model].append(record)

        return json.dumps(data, ensure_ascii=False)
