from django.test import TestCase
from database import backend, utils

class StudentTestCase(TestCase):
    def test_student_without_info(self):
        self.assertFalse(backend.check_student_information_filled(1))

    def test_student_with_unfinished_info(self):
        student_id = 2014000
        backend.set_student_information(student_id, real_name = '')
        self.assertFalse(backend.check_student_information_filled(student_id))

    def test_student_with_info(self):
        student_id = 2014000
        backend.set_student_information(student_id, real_name = 'doge')
        self.assertTrue(backend.check_student_information_filled(student_id))


class AdminTestCase(TestCase):
    def test_add_admin(self):
        username = 'wyl8899'
        password = 'correct'
        description = 'test description'
        self.assertTrue(backend.add_admin(username, password, description))
        self.assertEqual(Admin.all().count(), 1)
        admin = Admin.get()
        self.assertEqual(admin.username, username)
        self.assertEqual(admin.password, password)
        self.assertEqual(admin.description, description)

    def test_admins_with_same_name(self):
        username = 'wyl'
        self.assertTrue(backend.add_admin(username, 'xxx', 'des'))
        self.assertFalse(backend.add_admin(username, 'another', '?'))

    def test_check_admin_password(self):
        username = 'wyl8899'
        password = 'correct'
        backend.add_admin(username, password, 'description')
        self.assertTrue(backend.check_admin(username, password))
        self.assertFalse(backend.check_admin(username, 'wrong'))
