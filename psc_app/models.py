# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.conf import settings

# Create your models here.
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class Inscricao(AbstractBaseUser, PermissionsMixin):

	name = models.CharField('Nome', max_length=100, blank=False, null=False)
	email = models.EmailField('E-mail', unique=True)
	phone = models.CharField('Telefone', max_length=100, blank=True,null=True)
	image = models.ImageField(upload_to= 'media/imagens', verbose_name='Imagem',null = True, blank = True)
	username = models.CharField('Login', unique=True, max_length=100, null=True, blank=True)
	birth_data = models.CharField('Data de Nascimento', max_length=100,blank=True, null=True)
	sex = models.CharField('Sexo',max_length=1, choices=(('M', 'Masculino'), ('F', 'Feminino')), default='Feminino')
	is_active = models.BooleanField('Esta ativo?', blank=True, default=True)
	is_staff = models.BooleanField('E da equipe?', blank=True, default=False)
	date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)
	cpf = models.CharField('CPF', max_length=20, blank=True, null=True)
	curso = models.CharField('Curso', max_length=50, blank=False, null=False)
	area1 = models.CharField('Area de interesse 1', max_length=50, blank=True, null=True)
	area2 = models.CharField('Area de interesse 2', max_length=50, blank=True, null=True)
	turno = models.CharField('Turno da dinamica', max_length=20, blank=False, null=False)
	periodo = models.CharField('Periodo', max_length=20, blank=True, null=True)
	linkedin = models.URLField('Linkedin', blank=True, null=True)
	historico = models.FileField(upload_to= 'media/imagens', verbose_name='Historico', blank=False, null=False)
	curriculum = models.FileField(upload_to= 'media/imagens', verbose_name='Curriculum', blank=False, null=False)
	observacoes = models.TextField('Observacoes', blank=True, null=True)
	email_enviado = models.BooleanField('E-mail lembrando da dinamica', default=False, blank=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email','name']

	def __str__(self):
		return self.name

	def __unicode__(self):
		return u"username: %s " % (self.name or u'')

	def get_full_name(self):
		# The user is identified by their email address
		return self.username

	def get_short_name(self):
		# The user is identified by their email address
		return self.username

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	def set_enviado(self):
		this.email_enviado = True
		this.save()


class Periodo(models.Model):
	nome = models.CharField('Periodo', max_length=20, blank=True, null=True, unique=True)
	inscritos = models.ManyToManyField('Inscricao', related_name='inscritos', blank=True)

	def __str__(self):
		return self.nome


class Area(models.Model):
	nome = models.CharField('Periodo', max_length=30, blank=True, null=True, unique=True)
	descricao = models.TextField('Descricao', blank=True, null=True)

	def __str__(self):
		return self.nome