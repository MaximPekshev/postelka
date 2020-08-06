from django.shortcuts import render
from django.http import HttpResponse

def show_catalog(request):
	return HttpResponse('catalog')
	
