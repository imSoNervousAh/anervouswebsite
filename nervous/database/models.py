from django.db import models


class Admin(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=32)

    def __unicode__(self):
        return "%s: %s" % (self.username, self.description)


class OfficialAccount(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=300)

    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)


class Application(models.Model):
    official_account = models.OneToOneField(OfficialAccount, primary_key=True)
    user_submit = models.CharField(max_length=32)
    operator_admin = models.CharField(max_length=32)
    status = models.CharField(max_length=10)
    manager_name = models.CharField(max_length=30)
    manager_student_id = models.CharField(max_length=15)
    manager_dept = models.CharField(max_length=40)
    manager_tel = models.CharField(max_length=20)
    manager_email = models.CharField(max_length=254)
    association = models.CharField(max_length=30)

    def __unicode__(self):
        return "Application for %s from user %s, status: %s" % (
            self.official_account,
            self.user_submit,
            self.status
        )


class Article(models.Model):
    title = models.CharField(max_length=50)
    official_account_id = models.IntegerField()
    description = models.CharField(max_length=300, default='')
    views = models.IntegerField()
    likes = models.IntegerField()

    def __unicode__(self):
        return self.title
