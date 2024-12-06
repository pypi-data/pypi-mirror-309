import unittest
from string_helper import (
    to_camel_case,
    to_snake_case,
    generate_slug,
    truncate_string,
)

class TestStringHelpers(unittest.TestCase):
    def test_to_camel_case(self):
        self.assertEqual(to_camel_case("hello_world"), "helloWorld")

    def test_to_snake_case(self):
        self.assertEqual(to_snake_case("HelloWorld"), "hello_world")

    def test_generate_slug(self):
        self.assertEqual(generate_slug("Hello World!"), "hello-world")

    def test_truncate_string(self):
        self.assertEqual(truncate_string("Hello World", 5), "Hello...")
        self.assertEqual(truncate_string("Hello", 10), "Hello")
