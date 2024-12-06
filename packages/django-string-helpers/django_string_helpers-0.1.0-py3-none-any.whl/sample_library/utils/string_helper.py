from django.utils.text import slugify

def to_camel_case(string):
    """Convert a string to camelCase."""
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])

def to_snake_case(string):
    """Convert a string to snake_case."""
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()

def generate_slug(string):
    """Generate a URL-friendly slug."""
    return slugify(string)

def truncate_string(string, length):
    """Truncate a string to a specific length."""
    if len(string) <= length:
        return string
    return string[:length] + "..."
