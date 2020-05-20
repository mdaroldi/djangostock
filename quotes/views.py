from django.shortcuts import render, redirect
from quotes.models import Stock
from .iex_token import iex_publishable_token
from django.contrib import messages
from .forms import StockForm
import requests
import json


def home(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token"
                                   "=" + iex_publishable_token)
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker': "Enter a ticker symbol"})


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added!")
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            print("ticker: ", ticker_item, type(ticker_item))
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token"
                                                                                            "=" + iex_publishable_token)
            try:
                output.append(json.loads(api_request.content))
            except Exception as e:
                api = "Error..."
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "Stock has been deleted!")
    return redirect('delete_stock')


def delete_stock(request):
    ticker = Stock.objects.all()
    output = []
    for ticker_item in ticker:
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"
                                   + str(ticker_item) + "/quote?token="
                                   + iex_publishable_token)
        try:
            output.append(json.loads(api_request.content))
        except Exception as e:
            return redirect('delete_stock')
        except requests.exceptions.RequestException as e:
            return redirect('delete_stock')
    return render(request, 'delete_stock.html', {'ticker': ticker, 'output': output})
