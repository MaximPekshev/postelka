from django.shortcuts import render
from django.http import HttpResponse

from goodapp.models import Good, Picture
from goodapp.models import Category

from django.core.paginator import Paginator


class Item(object):
	
	good 		= Good
	main_image 	= Picture
	images 		= Picture


def get_categories(goods):

	all_caterories = Category.objects.all()

	categories = []

	for cat in all_caterories:
		if goods.filter(category=cat):
			categories.append(cat)

	categories.reverse()		

	return categories


def get_razmer_kpb_modifications(good):

	table = []

	goods = Good.objects.filter(parent_good=good, is_active=True)

	mod_goods = []

	if good.razmer_kpb not in table:
		table.append(good.razmer_kpb)
		mod_goods.append(good)

	for good in goods:
		if good.razmer_kpb not in table:
			table.append(good.razmer_kpb)
			mod_goods.append(good)

	return mod_goods
	
def get_razmer_navolocek_modifications(parent_good, good):

	goods = Good.objects.filter(parent_good=parent_good, razmer_kpb=good.razmer_kpb, is_active=True)

	table = []

	mod_goods = []

	if parent_good.razmer_navolocek not in table and parent_good.razmer_kpb == good.razmer_kpb:
		table.append(parent_good.razmer_navolocek)
		mod_goods.append(parent_good)

	for g in goods:
		if g.razmer_navolocek not in table:
			table.append(g.razmer_navolocek)
			mod_goods.append(g)

	return mod_goods


def get_razmer_prostyn_modifications(parent_good, good):

	table = []

	mod_goods = []

	if good.tip_prostyni == 'На резинке':

		goods = Good.objects.filter(parent_good=parent_good, razmer_kpb=good.razmer_kpb, is_active=True)


		if parent_good.razmer_prostyni not in table and parent_good.razmer_prostyni == good.razmer_prostyni:
			table.append(parent_good.razmer_prostyni)
			mod_goods.append(parent_good)

		for g in goods:
			if g.razmer_prostyni not in table:
				table.append(g.razmer_prostyni)
				mod_goods.append(g)

	return mod_goods


def show_category(request, cpu_slug):

	# if request.method == 'GET':

	# 	try:

	# 		request.GET['sort_by']

	# 		if request.GET['sort_by'] == 'name':

	# 			order_by='name'

	# 		elif request.GET['sort_by'] == 	'price':

	# 			order_by='price'
	# 	except:

	order_by='price'

	goods_count=18

	category = Category.objects.get(cpu_slug=cpu_slug)

	goods = Good.objects.filter(is_active=True, category=category,  is_modification=False, tip_prostyni='Обычная').order_by(order_by)

	table = []
	for good in goods:

		item = Item()
		
		item.good = good
		
		item.images = Picture.objects.filter(good=good).order_by('-main_image')

		item.main_image = item.images.first()
		 	
		table.append(item)

	page_number = request.GET.get('page', 1)

	paginator = Paginator(table, goods_count)	

	page = paginator.get_page(page_number)


	is_paginated = page.has_other_pages()

	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''	

	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''			


	template_name = 'goodapp/catalog.html'

	context = {

		'page_object': page,
		'prev_url': prev_url,
		'next_url': next_url,
		'is_paginated': is_paginated,
		'good_quantity': len(goods),
		'categories' : get_categories(Good.objects.filter(is_active=True, is_modification=False, tip_prostyni='Обычная').order_by('price')),
		'category': category,

	}


	return render(request, template_name, context)


def show_size(request, razmer_kpb):

	goods_count=18

	articles = []

	goods = []

	# goods = Good.objects.filter(is_active=True, razmer_kpb=razmer_kpb, tip_prostyni='Обычная').order_by('price')

	goods_with_razmer_kpb = Good.objects.filter(is_active=True, razmer_kpb=razmer_kpb, tip_prostyni='Обычная').order_by('price')

	for item in goods_with_razmer_kpb:

		if item.article not in articles:

			goods.append(item)

		articles.append(item.article)	



	table = []
	for good in goods:

		item = Item()
		
		item.good = good
		
		item.images = Picture.objects.filter(good=good).order_by('-main_image')

		item.main_image = item.images.first()
		 	
		table.append(item)

	page_number = request.GET.get('page', 1)

	paginator = Paginator(table, goods_count)	

	page = paginator.get_page(page_number)


	is_paginated = page.has_other_pages()

	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''	

	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''			


	template_name = 'goodapp/catalog.html'

	context = {

		'page_object': page,
		'prev_url': prev_url,
		'next_url': next_url,
		'is_paginated': is_paginated,
		'good_quantity': len(goods),
		'categories' : get_categories(Good.objects.filter(is_active=True, is_modification=False, tip_prostyni='Обычная').order_by('price')),
		'razmer_kpb': razmer_kpb,

	}


	return render(request, template_name, context)




def show_catalog(request):

	template_name = 'goodapp/category_list.html'

	context = {

		'categories' : get_categories(Good.objects.filter(is_active=True, is_modification=False, tip_prostyni='Обычная').order_by('price')),

	}


	return render(request, template_name, context)


def show_good(request ,slug):

	good = Good.objects.get(slug=slug)

	parent_good = Good.objects.filter(article=good.article, is_modification=False).first()

	pictures = Picture.objects.filter(good=good).order_by('-main_image')
	main_picture = pictures.first()


	template_name = 'goodapp/good.html'

	context = {

		'good' : good,
		'pictures' : pictures,
		'main_picture' : main_picture,
		'kpb_razmer_modifications': get_razmer_kpb_modifications(parent_good),
		'navolocek_razmer_modifications': get_razmer_navolocek_modifications(parent_good, good),
		'prostyn_razmer_modifications': get_razmer_prostyn_modifications(parent_good, good),
		'categories' : good.category.all(),

	}

	return render(request, template_name, context)