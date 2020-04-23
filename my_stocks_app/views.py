from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
	import requests 
	import json 

	if request.method == 'POST':
		stockItem = request.POST['stockItem']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + stockItem + "/quote?token=pk_736b456d7dcf4a2589d88cee4789e8c9")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error"
		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'stockItem': "Enter a stockItem Symbol Above..."})

def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
	import requests 
	import json 

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added!"))
			return redirect('add_stock')

	else:	
		stockItem = Stock.objects.all()
		output = []
		for stockItem_item in stockItem:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(stockItem_item) + "/quote?token=pk_736b456d7dcf4a2589d88cee4789e8c9")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error"
		
		return render(request, 'add_stock.html', {'stockItem': stockItem, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted!"))
	return redirect(delete_stock)



def delete_stock(request):
	stockItem = Stock.objects.all()
	return render(request, 'delete_stock.html', {'stockItem': stockItem})
