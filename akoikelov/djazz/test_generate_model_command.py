import os
from django.core.management import call_command
from django.test import TestCase
from mock import mock
from django.conf import settings


class RawInputMock(object):

    def mock_raw_input(self, question, field_name, field_type):
        if question.__contains__('Field name?'):
            return field_name
        elif question.__contains__('Field type?'):
            return field_type
        elif question.__contains__('Max length?'):
            return '1000'
        elif question.__contains__('Unique?[False]') or question.__contains__('Null?[False]'):
            return ''
        elif question.__contains__('Add more fields?[yes]'):
            return 'no'
        elif question.__contains__('Related model name?'):
            return ''
        elif question.__contains__('On delete?[models.CASCADE]'):
            return ''
        elif question.__contains__('ManyToMany model name?'):
            return 'TestManyToMany2'
        elif question.__contains__('Through model??'):
            return 'TestThroughModel'

    def primitive_field_mock(self, question):
        return self.mock_raw_input(question=question, field_type='char', field_name='title')

    def foreignkey_field_mock(self, question):
        return self.mock_raw_input(question=question, field_type='fkey', field_name='testForeignKey')

    def manytomany_field_mock(self, question):
        return self.mock_raw_input(question=question, field_type='mtm', field_name='testManyToMany')


class TestGenerateModelCommand(TestCase):

    def setUp(self):
        self.mock = RawInputMock()

        if not os.path.exists(settings.BASE_DIR + '/akoikelov_djazz_test_app'):
            call_command('startapp', 'akoikelov_djazz_test_app')

    def test_primitive_field(self):
        with mock.patch('__builtin__.raw_input', self.mock.primitive_field_mock):
            call_command('generate_model', 'akoikelov_djazz_test_app', 'TestPrimitive')

    def test_foreignkey_field(self):
        with mock.patch('__builtin__.raw_input', self.mock.foreignkey_field_mock):
            call_command('generate_model', 'akoikelov_djazz_test_app', 'TestForeignKey')

    def test_manytomany_field(self):
        with mock.patch('__builtin__.raw_input', self.mock.manytomany_field_mock):
            call_command('generate_model', 'akoikelov_djazz_test_app', 'TestManyToMany')