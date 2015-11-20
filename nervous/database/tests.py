from database import backend, utils
from models import *

from django.test import TestCase
from django.core.exceptions import ValidationError

class StudentTestCase(TestCase):
    def test_student_without_info(self):
        self.assertFalse(backend.check_student_information_filled(1))

    def test_student_with_unfinished_info(self):
        student_id = 2014000
        backend.set_student_information(student_id, {'real_name':''})
        self.assertFalse(backend.check_student_information_filled(student_id))

    def test_student_with_info(self):
        student_id = 2014000
        backend.set_student_information(student_id, {'real_name':'doge'})
        self.assertTrue(backend.check_student_information_filled(student_id))


class AdminTestCase(TestCase):
    def test_add_admin(self):
        username = 'wyl8899'
        password = 'correct'
        email = 'test_email@nervous.com'
        description = 'test description'
        self.assertTrue(backend.add_admin(username, password, email, description))
        self.assertEqual(Admin.objects.all().count(), 1)
        admin = Admin.objects.get()
        self.assertEqual(admin.username, username)
        self.assertEqual(admin.password, password)
        self.assertEqual(admin.description, description)

    def test_admins_with_same_name(self):
        username = 'wyl'
        email = 'test_email@nervous.com'
        self.assertTrue(backend.add_admin(username, 'xxx', email, 'des'))
        self.assertFalse(backend.add_admin(username, 'another', email, '?'))

    def test_check_admin_password(self):
        username = 'wyl8899'
        password = 'correct'
        email = 'test_email@nervous.com'
        backend.add_admin(username, password, email, 'description')
        self.assertTrue(backend.check_admin(username, password))
        self.assertFalse(backend.check_admin(username, 'wrong'))


class ApplicationTestCase(TestCase):
    def test_add_application_with_same_account_wx_id(self):
        wx_id = 'test_wx_id'
        app = {
            'name': 'name',
            'wx_id': wx_id,
            'description': 'description',
        }
        another_app = {
            'name': 'another_name',
            'wx_id': wx_id,
            'description': 'another description',
        }
        backend.add_application(app)
        with self.assertRaises(ValidationError):
            backend.add_application(another_app)

    def test_get_application_by_user_submit(self):
        username = 'hdd'
        acc_name = 'acc_name'
        app = {
            'name': acc_name,
            'wx_id': 'wx_id',
            'description': 'description',
            'user_submit': username,
        }
        another_app = {
            'name': 'another account name',
            'wx_id': 'another_wx_id',
            'description': 'by another user',
            'user_submit': 'not equal to hdd',
        }
        backend.add_application(app)
        backend.add_application(another_app)
        res = backend.get_applications_by_user(username)
        self.assertEqual(res.count(), 1)
        self.assertEqual(res.first().name(), acc_name)
