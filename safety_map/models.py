# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    protecter_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Danger(models.Model):
    danger_pk = models.IntegerField(primary_key=True)
    danger_type = models.CharField(max_length=30)
    danger_img = models.TextField()
    danger_loc = models.TextField()  # This field type is a guess.
    auth_user_id_fk = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='auth_user_id_fk', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'danger'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DongLevel(models.Model):
    objects = models.Manager()
    dong_level_pk = models.IntegerField(primary_key=True)
    dong_level_tot = models.IntegerField()
    dong_nm = models.CharField(max_length=30)
    dong_loc = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'dong_level'


class Female(models.Model):
    female_pk = models.AutoField(primary_key=True)
    female_crime_type = models.CharField(max_length=30, blank=True, null=True)
    female_crime_loc = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'female'


class Kid(models.Model):
    kid_pk = models.AutoField(primary_key=True)
    kid_accident_type = models.CharField(max_length=30)
    kid_accident_loc = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'kid'


class SafetyZone(models.Model):
    safety_zone_pk = models.AutoField(primary_key=True)
    safety_type = models.CharField(max_length=30)
    safety_loc = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'safety_zone'
