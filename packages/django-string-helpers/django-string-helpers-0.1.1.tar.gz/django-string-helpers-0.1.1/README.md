# Django String Helpers

A collection of string helper utilities for Django applications.

## Installation

Install via pip:

```bash
pip install django-string-helpers

INSTALLED_APPS = [
    # Other apps
    "django_string_helpers",
]

from django_string_helpers.string_helpers import to_camel_case

print(to_camel_case("hello_world"))  # Output: helloWorld
