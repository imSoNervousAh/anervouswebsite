from django.core.exceptions import ValidationError
from django.test import TestCase

from database import backend
from models import *


class StudentTestCase(TestCase):
    def test_student_without_info(self):
        self.assertFalse(backend.check_student_information_filled(1))

    def test_student_with_unfinished_info(self):
        student_id = 2014000
        self.assertFalse(backend.check_student_information_filled(student_id))

    def test_student_with_info(self):
        student_id = 2014000
        backend.set_student_information(student_id, {
            'real_name': 'doge',
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
    def setUp(self):
        self.default_name = 'name'
        self.default_wx_id = 'wx_id'
        self.default_description = 'description'
        self.default_user_submit = 'user_submit'
        default_app_dic = {
            'name': self.default_name,
            'wx_id': self.default_wx_id,
            'description': self.default_description,
            'user_submit': self.default_user_submit,
            'status': 'pending',
        }
        backend.add_application(default_app_dic)
        self.default_app = Application.objects.all().get()

    def test_add_application_with_same_account_wx_id(self):
        app_dic = {
            'name': 'name',
            'wx_id': self.default_wx_id,
            'description': 'description',
            'status': 'pending',
        }
        with self.assertRaises(ValidationError):
            backend.add_application(app_dic)

    def test_get_application_by_user_submit(self):
        acc_name = 'another_acc_name'
        user_submit = 'hdd'
        app_dic = {
            'name': acc_name,
            'wx_id': 'another_wx_id',
            'description': 'by another user',
            'user_submit': user_submit,
            'status': 'pending'
        }
        backend.add_application(app_dic)
        res = backend.get_applications_by_user(user_submit)
        self.assertEqual(res.count(), 1)
        app = res.first()
        self.assertEqual(app.name(), acc_name)
        self.assertEqual(app.user_submit, user_submit)

    def test_admin_modify_application(self):
        admin_name = 'admin'
        status = 'approved'
        backend.modify_application({
            'id': self.default_app.id,
            'operator_admin': admin_name,
            'status': status,
        })
        app = Application.objects.get()
        self.assertEqual(app.status, status)
        self.assertEqual(app.operator_admin, admin_name)

    def test_get_application_by_status(self):
        status = 'approved'
        backend.modify_application({
            'id': self.default_app.id,
            'status': status,
        })
        app_dic = {
            'name': 'name',
            'wx_id': 'another_wx_id',
            'description': 'description',
            'user_submit': 'another_user',
            'status': 'pending',
        }
        backend.add_application(app_dic)
        id = self.default_app.id
        res = backend.get_applications_by_status(status)
        self.assertEqual(res.count(), 1)
        self.assertEqual(res[0].id, id)

    def test_del_application(self):
        id = Application.objects.get().id
        backend.del_application(id)
        self.assertEqual(Application.objects.all().count(), 0)

    def test_recall_application(self):
        pass

    def test_get_applications(self):
        backend.get_applications()

    def test_get_pending_applications(self):
        backend.get_pending_applications()

    def test_student_modify_application(self):
        acc_name = 'acc_name_no2'
        user_submit = 'hdd_2'
        app_dic = {
            'name': acc_name,
            'wx_id': 'jiujiujiuwewewew',
            'description': 'by another user',
            'user_submit': user_submit,
            'status': 'pending'
        }
        backend.add_application(app_dic)
        res = backend.get_applications_by_status('pending')
        backend.recall_application(res[0].id())
        #res = backend.get_applications_by_status('not_submitted')
        app_dic['application_id'] = res[0].id()
        app_dic['status'] = 'not_submitted'
        backend.student_modify_application(app_dic)

    def test_get_applications_by_admin(self):
        backend.get_applications_by_admin('rsents')


class ArticleTest(TestCase):
    def test_get_articles(self):
        backend.get_articles()
    def test_get_articles_by_official_account_id(self):
        backend.get_articles_by_official_account_id(0)

class MessageTest(TestCase):
    def test_get_messages(self):
        backend.get_messages()
