
from .models import Good, Picture, Manufacturer, Category
import xlrd
from decimal import Decimal

def import_goods_citrade_xlsx():
	
	rb = xlrd.open_workbook('test.xlsx')
	sheet = rb.sheet_by_index(0)

	for rownum in range(sheet.nrows):

		good_id = str(Decimal(sheet.cell(rownum,6).value))

		try:
			good = Good.objects.get(kind_id=good_id)
		except Good.DoesNotExist:
			good = Good(kind_id=good_id)
			good.name = str(sheet.cell(rownum,0).value)
			good.save()

		if sheet.cell(rownum,7).value:

			good.is_modification = True

			try:
				parent_good = Good.objects.get(article=str(sheet.cell(rownum,3).value), is_modification=False)
				good.parent_good = parent_good
			except Good.DoesNotExist:
				pass
		else:
			
			good.is_modification = False				


		if sheet.cell(rownum,3).value:
			if good.article != str(sheet.cell(rownum,3).value):
				good.article = str(sheet.cell(rownum,3).value)

		if sheet.cell(rownum,8).value:
			if good.weight != str(sheet.cell(rownum,8).value):
				good.weight = str(sheet.cell(rownum,8).value)

		if sheet.cell(rownum,9).value:
			if good.dimensions != str(sheet.cell(rownum,9).value):
				good.dimensions = str(sheet.cell(rownum,9).value)

		if sheet.cell(rownum,10).value:
			if good.price != Decimal(sheet.cell(rownum,10).value):
				good.price = Decimal(sheet.cell(rownum,10).value)

		if sheet.cell(rownum,11).value:
			if good.razmer_kpb != str(sheet.cell(rownum,11).value):
				good.razmer_kpb = str(sheet.cell(rownum,11).value)

		if sheet.cell(rownum,12).value:
			if good.razmer_navolocek != str(sheet.cell(rownum,12).value):
				good.razmer_navolocek = str(sheet.cell(rownum,12).value)

		if sheet.cell(rownum,13).value:
			if good.razmer_prostyni != str(sheet.cell(rownum,13).value):
				good.razmer_prostyni = str(sheet.cell(rownum,13).value)		

		if sheet.cell(rownum,14).value:
			if good.tip_prostyni != str(sheet.cell(rownum,14).value):
				good.tip_prostyni = str(sheet.cell(rownum,14).value)

		if sheet.cell(rownum,17).value:
			if good.upakovka != str(sheet.cell(rownum,17).value):
				good.upakovka = str(sheet.cell(rownum,17).value)		

		if sheet.cell(rownum,19).value:
			if good.fabric != str(sheet.cell(rownum,19).value):
				good.fabric = str(sheet.cell(rownum,19).value)

		if sheet.cell(rownum,20).value:
			if good.duvet_cover_size != str(sheet.cell(rownum,20).value):
				good.duvet_cover_size = str(sheet.cell(rownum,20).value)


		if sheet.cell(rownum,5).value:

			categories = str(sheet.cell(rownum,5).value).split(',')

			for str_cat in categories:

				try:
					cat = Category.objects.get(name=str_cat)
				except Category.DoesNotExist:
					cat = Category(name=str_cat)
					cat.save()

				if cat in good.category.all():
					pass
				else:	
					good.category.add(cat)


		if sheet.cell(rownum,1).value:

			str_manufacturer = str(sheet.cell(rownum,1).value)

			try:
				manufacturer = Manufacturer.objects.get(name=str_manufacturer)
			except Manufacturer.DoesNotExist:
				manufacturer = Manufacturer(name=str_manufacturer)
				manufacturer.save()

			good.manufacturer = manufacturer


		good.save()

		if sheet.cell(rownum,2).value:
			images = str(sheet.cell(rownum,2).value).split(',')
			for im in images:
				try:
					picture = Picture.objects.get(good=good, image_url=im.strip())
				except Picture.DoesNotExist:			
					picture = Picture(
						good=good, 
						image_url=im.strip()
						)
					picture.save()
		

def upload_price_citrade():

	rb = xlrd.open_workbook('ostatki_2020.xlsx')
	sheet = rb.sheet_by_index(0)

	for rownum in range(sheet.nrows):

		good_id = str(Decimal(sheet.cell(rownum,0).value))

		try:
			good = Good.objects.get(kind_id=good_id)

			if sheet.cell(rownum,1).value:
				if good.quantity != Decimal(sheet.cell(rownum,1).value):
					good.quantity = Decimal(sheet.cell(rownum,1).value)
					if good.quantity:
						good.is_active = True

			if sheet.cell(rownum,2).value:
				if good.price != Decimal(sheet.cell(rownum,2).value):
					good.price = Decimal(sheet.cell(rownum,2).value)		

			good.save()

		except Good.DoesNotExist:
			pass