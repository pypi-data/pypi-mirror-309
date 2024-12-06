# Django String Helpers

A collection of string helper utilities for Django applications.

## Installation

Install via pip:

```bash
pip install django-string-helpers
```

```bash
INSTALLED_APPS = [
    # Other apps
    "django_string_helpers",
]
```

```bash
from django_string_helpers.string_helper import to_camel_case

print(to_camel_case("hello_world"))  # Output: helloWorld
```