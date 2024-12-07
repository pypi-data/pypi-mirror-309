from django.test import TestCase, override_settings


# Sample - you can override any settings you require for your tests
# @override_settings(ROOT_URLCONF='exceptional_auth.tests.urls')
class MyTestCase(TestCase):
    def test_things_import(self):
        import exceptional_auth
