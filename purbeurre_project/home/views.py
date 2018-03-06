from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .OFFData import OFFData
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def search(request):
    query = request.GET.get('query')

    data = OFFData(query)
    if not data.get_product():
        return None
    products = data.get_substitutes()
    context = {
        'query': query,
        'product': data.product,
        'products': products
    }
    return render(request, 'home/search.html', context)

def favorites(request):
    template = loader.get_template('home/favorites.html')
    return HttpResponse(template.render(request=request))

def account(request):
    template = loader.get_template('home/account.html')
    return HttpResponse(template.render(request=request))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'home/signup.html', {'form': form})

def product(request, id):
    product = Product.objects.get(id_off=id)
    context = {
        'product': product,
        'nutriscore': ['A', 'B', 'C', 'D', 'E']
    }
    return render(request, 'home/product.html', context)