# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.core.validators import *
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
import traceback


# Utils

def get_field(model_instance, field_name):
    return model_instance._meta.get_field_by_name(field_name)[0]


def get_field_verbose_name(model_instance, field_name):
    return get_field(model_instance, field_name).verbose_name


# Who knows

class NervousModel(models.Model):
    @classmethod
    def from_dict(cls, dic, base=None):
        """
            Construct a model instance from a python dict, using the fields
            given in the dict and do not set other fields, or, if `base`
            given, override the corresponding fields of the existing model
            instance `base`.

            If an invalid field name is given (i.e. no such field), the
            proposed value of that field is ignored.

            Every field that is to be written will be validated, this is
            done by calling `clean_fields` excluding the fields untouched.

            Note that in order to handle ForeignKeys properly, we adopted
            the approach used by Django: if the dict has an element {
            'model_key__name': 'some_name'}, the field `model_key` will
            be become the value of `Model.get(name='some_name')`, where
            `Model` is the model class to which `model_key` the ForeignKey
            referencing.
        """

        manager = cls.objects
        meta = cls._meta
        model = base or manager.model()
        exclude = [field.name for field in meta.fields]
        for (key, val) in dic.iteritems():
            try:
                # extract the field name and leave the rest as kwargs passed
                # to Django in case '__' presents
                keys = str(key).split('__', 1)
                field_name = keys[0]
                field = cls._meta.get_field(field_name)
                if len(keys) == 1:
                    # ordinary field
                    raw_val = val
                else:
                    # ForeignKey
                    rel_cls = cls._meta.get_field(field_name).rel.to
                    rel_manager = rel_cls.objects
                    rel_key = keys[1]
                    query_args = {rel_key: val}
                    raw_val = rel_manager.get(**query_args)
                setattr(model, field_name, raw_val)
                exclude.remove(field_name)
            except (FieldDoesNotExist,  # invalid field name
                    AttributeError,  # not a ForeignKey
                    ObjectDoesNotExist,  # `get` fails
                    MultipleObjectsReturned):  # `get` fails
                if settings.DEBUG:
                    traceback.print_exc()
        # let caller function handle ValidationErrors
        model.clean_fields(exclude=exclude)
        return model

    class Meta:
        abstract = True


# Enums

class SortOrder:
    Ascending, Descending = xrange(2)


class SortBy:
    Time, Likes, Views = xrange(3)


class MessageCategory:
    All, ToStudent, ToAdmin = xrange(3)


class ForewarnTarget:
    ViewsTotal, LikesTotal = xrange(2)


class NotificationOption:
    Email, Message = xrange(2)


# Models

class Admin(models.Model):
    username = models.CharField(u'该用户名', max_length=20, primary_key=True)
    description = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=254)

    class Meta:
        verbose_name = u'管理员'
        verbose_name_plural = u'管理员'

    def clean(self):
        if self.username == settings.SUPERUSER_USERNAME:
            raise ValidationError({
                'username': u'用户名不能与超级管理员相同'
            })

    def __unicode__(self):
        return "%s: %s" % (self.username, self.description)


class Student(models.Model):
    student_id = models.CharField(max_length=20, primary_key=True)
    real_name = models.CharField(max_length=20)
    dept = models.CharField(max_length=40)
    tel = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\d{3,12}$',
                message='请输入一个合法的电话号码'
            )
        ]
    )
    email = models.CharField(
        max_length=254,
        validators=[
            EmailValidator(
                message='请输入一个合法的邮件地址'
            )
        ]
    )

    class Meta:
        verbose_name = u'学生'
        verbose_name_plural = u'学生'

    def information_filled(self):
        try:
            self.full_clean()
            return True
        except ValidationError:
            return False

    def __unicode__(self):
        return u'%s(%s)' % (self.student_id, self.real_name)


class OfficialAccount(models.Model):
    wx_id = models.CharField(u'公众号微信ID', max_length=50, unique=True)
    name = models.CharField(u'公众号名称', max_length=40)
    description = models.CharField(u'公众号简介', max_length=300)
    likes_total = models.IntegerField(null=True, blank=True)
    views_total = models.IntegerField(null=True, blank=True)
    wci = models.FloatField(null=True, blank=True)

    """
        NOTE: Any account in a state other than NORMAL will prevent the
        whole table from being modified. At least we hope so, to get rid
        of concurrency problems.

        PENDING_CHECK state indicates the update actually changed
        something, may it be WCI, likesnum or other information.
        The account should enter FINISHED state otherwise.
    """
    NORMAL_STATUS = 0
    PENDING_UPDATE_STATUS = 1
    UPDATING_STATUS = 2
    UPDATED_STATUS = 3
    PENDING_CHECK_STATUS = 4
    FINISHED_STATUS = 5

    UPDATING_STATUS_CHOICES = (
        (NORMAL_STATUS, 'normal'),
        (PENDING_UPDATE_STATUS, 'pending_update'),
        (UPDATING_STATUS, 'updating'),
        (UPDATED_STATUS, 'updated'),
        (PENDING_CHECK_STATUS, 'pending_check'),
        (FINISHED_STATUS, 'finished')
    )
    update_status = models.IntegerField(
        choices=UPDATING_STATUS_CHOICES,
        default=NORMAL_STATUS
    )

    class Meta:
        verbose_name = u'微信公众号'
        verbose_name_plural = u'微信公众号'

    def latest_record(self):
        try:
            return self.accountrecord_set.order_by('-date')[0]
        except ObjectDoesNotExist:
            return None

    def unprocessed_messages_count(self, category):
        return self.message_set \
            .filter(
            processed__exact=False,
            category__exact=category
        ).count()

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.wx_id)


class AccountRecord(models.Model):
    account = models.ForeignKey(OfficialAccount)
    date = models.DateField()
    likes = models.IntegerField()
    views = models.IntegerField()
    articles = models.IntegerField()
    wci = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return "%s at %s" % (self.account.name, self.date)


class Application(models.Model):
    official_account = models.OneToOneField(OfficialAccount)
    user_submit = models.CharField(max_length=32)
    operator_admin = models.CharField(max_length=32, blank=True)
    reject_reason = models.CharField(max_length=140, blank=True)
    status = models.CharField(max_length=20)
    manager_name = models.CharField(max_length=30)
    manager_student_id = models.CharField(max_length=15)
    manager_dept = models.CharField(max_length=40)
    manager_tel = models.CharField(max_length=20)
    manager_email = models.CharField(max_length=254)
    association = models.CharField(max_length=30)

    def clean(self):
        if self.status not in ['approved', 'rejected', 'pending', 'not_submitted']:
            raise ValidationError({
                'status': 'Invalid status'
            })
        if self.status == 'rejected' and len(self.reject_reason) == 0:
            raise ValidationError({
                'reject_reason': '请填写拒绝理由'  # 'Rejected application should have a reason'
            })

    def status_display(self):
        names = {
            'approved': '已通过审批',
            'rejected': '审批被拒绝',
            'pending': '待审批',
            'not_submitted': '尚未提交',
        }
        icons = {
            'approved': 'fa-check-circle',
            'rejected': 'fa-times-circle',
            'pending': 'fa-question-circle',
            'not_submitted': 'fa-info-circle',
        }
        classes = {
            'approved': 'success',
            'rejected': 'danger',
            'pending': 'warning',
            'not_submitted': 'default',
        }
        status = str(self.status)
        return {
            'icon': icons[status],
            'name': names[status],
            'colorclass': classes[status]
        }

    def __unicode__(self):
        return u"Application for %s from user %s, status: %s" % (
            self.official_account,
            self.user_submit,
            self.status
        )


class Article(models.Model):
    title = models.CharField(max_length=50)
    official_account_id = models.IntegerField()
    description = models.CharField(max_length=300, default='')
    avatar_url = models.CharField(max_length=300, default='')
    url = models.CharField(max_length=300, unique=True)
    likes = models.IntegerField()
    views = models.IntegerField()
    posttime = models.DateTimeField()

    def official_account_name(self):
        return OfficialAccount.objects.get(pk=self.official_account_id).name

    def __unicode__(self):
        return self.title


class Message(models.Model):
    official_account = models.ForeignKey(OfficialAccount)
    category = models.IntegerField()  # value should come from MessageCategory
    content = models.CharField(max_length=140)
    processed = models.BooleanField()
    admin = models.ForeignKey(Admin, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def from_real_name(self):
        if self.category == MessageCategory.ToAdmin:
            return self.official_account.user_submit()
        else:
            try:
                return self.admin.description
            except:
                return "unknown admin"

    def datetime(self):
        return self.time

    def __unicode__(self):
        if self.category == MessageCategory.ToAdmin:
            direction = 'from'
        else:
            direction = 'to'
        return "%s under account %s %s %s, processed = %s" % (
            self.content,
            self.official_account.name,
            direction,
            self.official_account.application.user_submit,
            self.processed
        )


class ForewarnRule(NervousModel):
    account = models.ForeignKey(OfficialAccount, null=True, blank=True)
    duration = models.IntegerField(validators=[
        MinValueValidator(1, message=u'预警时限至少为1天'),
        MaxValueValidator(365, message=u'预警时限至多为365天'),
    ])
    notification = models.IntegerField()
    target = models.IntegerField()
    value = models.IntegerField(validators=[
        MinValueValidator(1, message=u'该值应为正数'),
        MaxValueValidator(2147483647, message=u'该值应在32位整数范围内'),
    ])
    time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.notification in [
            NotificationOption.Email,
            NotificationOption.Message]:
            raise ValidationError({
                'notification': 'Invalid notification option',
            })
        if not self.target in [
            ForewarnTarget.LikesTotal,
            ForewarnTarget.ViewsTotal]:
            raise ValidationError({
                'target': 'Invalid forewarn target',
            })

    def account_name(self):
        if self.account:
            return self.account.name
        else:
            return u'所有公众号'

    def notification_name(self):
        if self.notification == NotificationOption.Email:
            return u'邮件'
        elif self.notification == NotificationOption.Message:
            return u'站内通知'

    def __unicode__(self):
        return u"[%s, %s] for %s" % (
            self.target,
            self.value,
            self.account_name()
        )


class ForewarnRecord(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(OfficialAccount)
    target = models.IntegerField()
    value = models.IntegerField()

    def account_name(self):
        return self.account.name

    def __unicode__(self):
        return u'[%s, %s] by %s at %s' % (
            self.target,
            self.value,
            self.account_name(),
            self.datetime
        )


class Globals(models.Model):
    announcement = models.CharField(max_length=256, default='')


# Add delegating attributes

def add_delegate(cls, dest, key):
    def inner_delegate(self):
        return getattr(getattr(self, dest), key)

    setattr(cls, key, inner_delegate)


for attr in [
    'manager_name',
    'manager_student_id',
    'manager_dept',
    'manager_tel',
    'manager_email',
    'association',
    'user_submit',
]:
    add_delegate(OfficialAccount, 'application', attr)

for attr in ['name', 'description']:
    add_delegate(Application, 'official_account', attr)
