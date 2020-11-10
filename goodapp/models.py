from django.db import models

import os

from django.conf import settings

import uuid

from uuslug import slugify

def get_uuid():
	return str(uuid.uuid4().fields[0])


class Good(models.Model):

	name 				= models.CharField(max_length = 150, verbose_name='Наименование')
	description 		= models.TextField(max_length=2048, verbose_name='Описание', blank=True)

	meta_title 			= models.CharField(max_length=150, verbose_name='meta name', blank=True, null=True)
	meta_description 	= models.TextField(max_length=1024, verbose_name='meta description', blank=True, null=True)

	price 				= models.DecimalField(verbose_name='Цена', max_digits=15, decimal_places=0, blank=True, null=True)
	old_price			= models.DecimalField(verbose_name='Старая цена', max_digits=15, decimal_places=0, blank=True, null=True)

	article 			= models.CharField(max_length = 36, verbose_name='Артикул', blank=True, null=True, default='')

	dimensions 			= models.CharField(max_length = 36, verbose_name='Габариты', blank=True, null=True, default='')

	razmer_kpb			= models.CharField(max_length = 36, verbose_name='Размер', blank=True, null=True, default='')

	razmer_navolocek 	= models.CharField(max_length = 36, verbose_name='Размер наволочек', blank=True, null=True, default='')

	tip_prostyni		= models.CharField(max_length = 36, verbose_name='Тип простыни', blank=True, null=True, default='')

	razmer_prostyni		= models.CharField(max_length = 36, verbose_name='Размер простыни', blank=True, null=True, default='')

	upakovka			= models.CharField(max_length = 36, verbose_name='Упаковка', blank=True, null=True, default='')
	fabric				= models.CharField(max_length = 36, verbose_name='Состав', blank=True, null=True, default='')

	duvet_cover_size 	= models.CharField(max_length = 36, verbose_name='Размер пододеяленика', blank=True, null=True, default='')

	kind_id				= models.CharField(max_length = 36, verbose_name='Код производителя', blank=True, null=True, default='')

	quantity			= models.DecimalField(verbose_name='Остаток', max_digits=15, decimal_places=0, blank=True, null=True)
	weight				= models.CharField(max_length = 36, verbose_name='Вес', blank=True, null=True, default='')
	
	good_uid 			= models.CharField(max_length=36, verbose_name='Код', blank=True, null=True)

	slug 				= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)

	is_active			= models.BooleanField(verbose_name='Активен', default=False)

	cpu_slug			= models.SlugField(max_length=70, verbose_name='ЧПУ_Url', blank=True, db_index=True)

	parent_good 		= models.ForeignKey('Good', verbose_name='Родительский товар', on_delete=models.SET_DEFAULT,null=True, blank=True, default=None)

	is_modification		= models.BooleanField(verbose_name='Модификация', default=False)

	manufacturer 		= models.ForeignKey('Manufacturer', verbose_name='Производитель', on_delete=models.SET_DEFAULT,null=True, blank=True, default=None)

	category 			= models.ManyToManyField('Category', verbose_name='Категории')

	def __str__(self):

		return self.name

	def save(self, *args, **kwargs):

		if self.slug == "":
			self.slug = get_uuid()

		self.cpu_slug = '{}'.format(slugify(self.name + '_' + self.razmer_kpb + '_' + self.razmer_navolocek))	

		super(Good, self).save(*args, **kwargs)
			
	
	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'


class Manufacturer(models.Model):

	name 				= models.CharField(max_length = 150, verbose_name='Наименование')
	description 		= models.TextField(max_length=2048, verbose_name='Описание', blank=True)

	meta_title 			= models.CharField(max_length=150, verbose_name='meta name', blank=True, null=True)
	meta_description 	= models.TextField(max_length=1024, verbose_name='meta description', blank=True, null=True)

	slug 				= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)

	cpu_slug			= models.SlugField(max_length=70, verbose_name='ЧПУ_Url', blank=True, db_index=True)
		
	def __str__(self):

		return self.name

	def save(self, *args, **kwargs):

		if self.slug == "":
			self.slug = get_uuid()

		self.cpu_slug = '{}'.format(slugify(self.name))	

		super(Manufacturer, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Производитель'
		verbose_name_plural = 'Производители'


def get_image_name(instance, filename):
	
	new_name = ('%s' + '.' + filename.split('.')[-1]) % instance.slug
	return new_name


class Category(models.Model):

	name 				= models.CharField(max_length = 150, verbose_name='Наименование')

	meta_title 			= models.CharField(max_length=150, verbose_name='meta name', blank=True, null=True)
	meta_description 	= models.TextField(max_length=1024, verbose_name='meta description', blank=True, null=True)

	slug 				= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)
	cpu_slug			= models.SlugField(max_length=70, verbose_name='ЧПУ_Url', blank=True, db_index=True)
	parent_category 	= models.ForeignKey('Category', verbose_name='Категория', on_delete=models.SET_DEFAULT,null=True, blank=True, default=None)
	picture				= models.ImageField(upload_to=get_image_name, verbose_name='Изображение 370x334', default=None, null=True, blank=True)


	def __str__(self):

		return self.name

	def save(self, *args, **kwargs):

		if self.slug == "":
			self.slug = get_uuid()

		self.cpu_slug = '{}'.format(slugify(self.name))	

		super(Category, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'


class Picture(models.Model):

	title 					= models.CharField(max_length=150, verbose_name='Наименование', blank=True)
	slug 					= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)
	good 					= models.ForeignKey('Good', verbose_name='Товар', on_delete=models.CASCADE)
	images					= models.ImageField(upload_to=get_image_name, verbose_name='Изображение 550x685', default=None)
	image_url				= models.CharField(max_length=150, verbose_name='Ссылка', blank=True)
	main_image				= models.BooleanField(verbose_name='Основная картинка', default=False)

	def __str__(self):
		
		return self.slug

	def save(self, *args, **kwargs):
		
		if self.slug == "":
			self.slug = get_uuid()
			self.title = self.slug

		super(Picture, self).save(*args, **kwargs)

	class Meta:
		
		verbose_name = 'Картинка'
		verbose_name_plural = 'Картинки'		