from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .OFFData import OFFData
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email

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
    if request.user.is_authenticated:
        if request.method == 'POST' and 'emailchange' in request.POST:
            try:
                validate_email(request.POST.get('email'))
                request.user.email = request.POST.get('email')
                request.user.save()
            except Exception:
                pass
        return render(request, 'home/account.html')
    return render(request, 'home/notlogged.html')

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

def saveproduct(request, id):
    if request.user.is_authenticated:
        # Check if not already fav
        try:
            product = request.user.profile.favorites.get(id_off=id)
        except Product.DoesNotExist:
            try:
                product = Product.objects.get(id_off=id)
                request.user.profile.favorites.add(product)
                return JsonResponse({'state':'success', 'action': 'added'}, status=200)
            except Product.DoesNotExist:
                return JsonResponse({'state':'error', 'action': 'added'}, status=400)

        request.user.profile.favorites.remove(product)
        return JsonResponse({'state':'success', 'action': 'removed'}, status=200)
    else:
        return JsonResponse({'state':'error', 'reason': 'User not logged in', 'action': 'null'}, status=400)