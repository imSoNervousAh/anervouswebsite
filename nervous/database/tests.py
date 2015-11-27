from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test import override_settings

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

    def test_get_student_by_id(self):
        student_id = 2014000
        backend.set_student_information(student_id, {
            'real_name': 'doge',
            'tel': '110',
            'dept': 'dept',
            'email': 'a@bc.com',
        })
        res = backend.get_student_by_id(2014000)
        self.assertEqual(2014000, res.student_id)


class AdminTestCase(TestCase):
    def test_add_admin(self):
        username = 'wyl8899'
        password = 'correct'
        email = 'test_email@nervous.com'
        description = 'test description'
        backend.add_admin(username, password, email, description)
        self.assertEqual(backend.get_admins().count(), 1)
        admin = Admin.objects.get()
        self.assertEqual(admin.username, username)
        self.assertEqual(admin.password, password)
        self.assertEqual(admin.description, description)

    def test_admins_with_same_name(self):
        username = 'wyl'
        email = 'test_email@nervous.com'
        backend.add_admin(username, 'xxx', email, 'des')
        with self.assertRaises(ValidationError):
            backend.add_admin(username, 'another', email, '?')

    def test_check_admin_password(self):
        username = 'wyl8899'
        password = 'correct'
        email = 'test_email@nervous.com'
        backend.add_admin(username, password, email, 'description')
        self.assertTrue(backend.check_admin(username, password))
        self.assertFalse(backend.check_admin(username, 'wrong'))
        self.assertFalse(backend.check_admin(username + 'asdasda', password))

    def test_del_admin(self):
        username = 'rsents'
        password = 'correct'
        email = 'test_email@nervous.com'
        description = 'test description'
        backend.add_admin(username, password, email, description)
        self.assertEqual(backend.get_admins().count(), 1)
        admin = Admin.objects.get()
        self.assertEqual(admin.username, username)
        self.assertEqual(admin.password, password)
        self.assertEqual(admin.description, description)
        self.assertTrue(backend.del_admin('rsents'))
        self.assertFalse(backend.del_admin('rsents12321312312'))

    def test_get_admin_emails(self):
        backend.get_admin_emails()


@override_settings(ALLOW_INVALID_WX_NAME=True)
@override_settings(UPDATE_UPON_APPROVING=False)
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
        backend.recall_application(id)
        backend.del_application(id)
        self.assertEqual(Application.objects.all().count(), 0)
        with self.assertRaises(Exception):
            backend.del_application(id)

    def test_get_applications(self):
        backend.get_applications()

    def test_get_pending_applications(self):
        backend.get_pending_applications()

    def test_student_modify_application(self):
        id = self.default_app.id
        backend.recall_application(id)
        app_dic = {
            'id': id,
            'status': 'not_submitted',
        }
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

    def test_process_all_messages(self):
        self.assertTrue(backend.process_all_messages(0, 0))

    def test_add_messages(self):
        username = 'rsents'
        password = '1231231'
        email = 'a@bc.com'
        description = 'no'
        backend.add_admin(username, password, email, description)
        x = OfficialAccount.objects.create(wx_id='jiujingzixun')
        backend.add_message(MessageCategory.ToStudent, x.id, 'hahaha', 'rsents')


class NervousTest(TestCase):
    def test_get_lastest_record_date(self):
        x = OfficialAccount.objects.create(wx_id='jiujingzixun')
        backend.get_lastest_record_date(x)

    def test_del_official_account(self):
        test_account = OfficialAccount.objects.create(wx_id='jiujingzixun')
        test_id = test_account.id
        backend.del_official_account(test_id)
        with self.assertRaises(Exception):
            backend.del_official_account(test_id)

    def test_check_forewarn_rule_on_account(self):
        test_account = OfficialAccount.objects.create(wx_id='jiujingzixun')
        x = ForewarnRule.objects.create(account=test_account,target=10,notification=10,value=10,duration=10)
        backend.check_forewarn_rule_on_account(x, test_account)

    def test_check_forewarn_rule(self):
        test_account = OfficialAccount.objects.create(wx_id='jiujingzixun')
        x = ForewarnRule.objects.create(account=test_account,target=10,notification=10,value=10,duration=10)
        backend.check_forewarn_rule(x, test_account)

    def test_forewarn_rule_from_dict(self):
        dic = {}
        ac_name = 'qwerty'
        dic['account_name'] = ac_name
        test_account = OfficialAccount.objects.create(name=ac_name)
        dic['duration'] = 10
        dic['notification'] = 1
        dic['target'] = 0
        dic['value'] = 1
        x = backend.forewarn_rule_from_dict(dic)
        self.assertEqual(x.account.name, dic['account_name'])
        self.assertEqual(x.duration, dic['duration'])
        self.assertEqual(x.notification, dic['notification'])
        self.assertEqual(x.target, dic['target'])
        self.assertEqual(x.value, dic['value'])

    def test_check_all_forewarn_rules(self):
        ac_name = 'qwerty'
        test_account = OfficialAccount.objects.create(name=ac_name)
        x = ForewarnRule.objects.create(account=test_account,target=10,notification=10,value=10,duration=10)
        x.save()
        x = ForewarnRule.objects.create(account=test_account,target=10,notification=5,value=10,duration=10)
        x.save()
        backend.check_all_forewarn_rules()

    def test_updating_account_name(self):
        backend.updating_account_name()
