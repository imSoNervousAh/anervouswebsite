from database import backend, utils
from models import *

from django.test import TestCase
from django.core.exceptions import ValidationError

class StudentTestCase(TestCase):
    def test_student_without_info(self):
        self.assertFalse(backend.check_student_information_filled(1))


    def test_student_with_unfinished_info(self):
        student_id = 2014000
        self.assertFalse(backend.check_student_information_filled(student_id))


    def test_student_with_info(self):
        student_id = 2014000
        backend.set_student_information(student_id, {
            'real_name':'doge',
            'tel': '110',
            'dept': 'dept',
            'email': 'a@bc.com',
        })
        self.assertTrue(backend.check_student_information_filled(student_id))


class AdminTestCase(TestCase):
    def test_add_admin(self):
        username = 'wyl8899'
        password = 'correct'
        email = 'test_email@nervous.com'
        description = 'test description'
        self.assertTrue(backend.add_admin(username, password, email, description))
        self.assertEqual(backend.get_admins().count(), 1)
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


    def test_admin_modify_application(self):
        admin_name = 'admin'
        status = 'accepted'
        dic = {
            'name': 'name',
            'wx_id': 'wx_id',
            'description': 'description',
            'user_submit': 'user_submit',
        }
        backend.add_application(dic)
        backend.modify_application({
            'account_id': Application.objects.get().id,
            'operator_admin': admin_name,
            'status': status,
        })
        app = Application.objects.get()
        self.assertEqual(app.status, status)
        self.assertEqual(app.operator_admin, admin_name)


    def test_get_application_by_status(self):
        user = 'user'
        status = 'accepted'
        app_dic = {
            'name': 'name',
            'wx_id': 'wx_id',
            'description': 'description',
            'user_submit': user,
        }
        another_app_dic = {
            'name': 'name',
            'wx_id': 'another_wx_id',
            'description': 'description',
            'user_submit': 'another_user',
        }
        backend.add_application(app_dic)
        backend.add_application(another_app_dic)
        id = backend.get_applications_by_user(user)[0].id()
        backend.modify_application({
            'account_id': id,
            'status': status,
        })
        res = backend.get_applications_by_status(status)
        self.assertEqual(res.count(), 1)
        self.assertEqual(res[0].id(), id)
