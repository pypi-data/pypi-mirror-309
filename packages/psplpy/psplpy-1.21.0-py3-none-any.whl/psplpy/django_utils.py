import django
from django.conf import settings
from django.db import models, connections
from psplpy.image_det import TxtProc


class Database:
    SQLITE3 = 'django.db.backends.sqlite3'
    POSTGRESQL = 'django.db.backends.postgresql'
    MYSQL = 'django.db.backends.mysql'

    def __init__(self, engine=SQLITE3, name=None, user=None, password=None,
                 host='localhost', port=None, app_label: str = '', **django_settings):
        databases = {
            'default': {
                'ENGINE': engine,
                'NAME': name,
                'USER': user,
                'PASSWORD': password,
                'HOST': host,
                'PORT': port,
                'APP_LABEL': app_label,
            }
        }

        # Update the settings with the custom DATABASES dictionary
        settings_dict = {'DATABASES': databases}
        settings_dict.update(django_settings)
        settings.configure(**settings_dict)
        # Initialize Django
        django.setup()

        # Create the custom base model
        class CustomBaseModel(models.Model):
            class Meta:
                app_label = databases['default']['APP_LABEL']
                abstract = True

            @classmethod
            def init(cls, new_name=None) -> None:
                Database.change_table_name(cls, new_name)
                Database.create_table(cls)
                Database.update_table(cls)

        self.Model = CustomBaseModel

    @staticmethod
    def change_table_name(model, new_name=None) -> None:
        if new_name is None:
            new_name = TxtProc.camel_to_snake(model.__name__)
        model._meta.db_table = new_name

    @staticmethod
    # Create a table if it doesn't exist
    def create_table(model) -> None:
        with connections['default'].schema_editor() as schema_editor:
            if model._meta.db_table not in connections['default'].introspection.table_names():
                schema_editor.create_model(model)

    @staticmethod
    # Update table if you added fields (doesn't drop fields as far as i know, which i was too afraid to implement)
    def update_table(model) -> None:
        with connections['default'].schema_editor() as schema_editor:
            if model._meta.db_table not in connections['default'].introspection.table_names():
                raise ValueError(f'Table "{model._meta.db_table}" not found.')
            else:
                # Get the database columns
                database_columns = connections['default'].introspection.get_table_description(
                    connections['default'].cursor(), model._meta.db_table)
                database_column_names = [column.name for column in database_columns]
                # Check if each field in the model exists in the database table
                for field in model._meta.fields:
                    if field.column not in database_column_names:
                        # Add the new column to the table
                        schema_editor.add_field(model, field)
