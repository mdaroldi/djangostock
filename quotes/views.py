from django.shortcuts import render
from quotes.models import Stock
from .iex_token import iex_publishable_token


def home(request):
    import requests
    import json

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

    ticker = Stock.objects.all()
    return render(request, 'add_stock.html', {'ticker': ticker})