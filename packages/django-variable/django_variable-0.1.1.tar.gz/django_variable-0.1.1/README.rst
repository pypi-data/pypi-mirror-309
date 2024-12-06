# Django Variable

django_variable is a library to define dynamic global settings
that can be set within a regular django form and edited
within django's admin panel.

## How it works

Set the config values using admin (admin/variable_config/configuration/)
Those values are persisted in the database (one per row)
and stored in an in-memory cache for later access.

## Compatibility

* Python +3.8
* Django >= 5

## Documentation

[Read The Docs](http://django-variable.readthedocs.org)

## License

MIT