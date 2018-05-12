from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.template import loader
from .OFFData import OFFData
from .models import Product, Profile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
import secrets


def index(request):
    """Return Index View"""
    return render(request, 'home/index.html')


def search(request):
    """Return Search View"""
    query = request.GET.get('query')

    if not query:
        return redirect('/')

    data = OFFData(query)
    if not data.get_product():
        return render(request, 'home/noresult.html', {'query': query})

    products = data.get_substitutes()
    context = {
        'query': query,
        'product': data.product,
        'products': sorted(products, key=lambda product: product.nutrition_grade)
    }

    return render(request, 'home/search.html', context)


def favorites(request):
    """Return Favorites View"""
    if request.user.is_authenticated:
        # Create Unique Token for favorites API
        if not request.user.profile.api_token:
            request.user.profile.api_token = secrets.token_urlsafe(20)
            request.user.save()
        return render(request, 'home/favorites.html')
    return render(request, 'home/notlogged.html', status=401)

def favoritesjson(request, token):
    try:
        profile = Profile.objects.get(api_token=token)
        queryset = profile.favorites.all()
        if not queryset:
            return JsonResponse({'state': 'success', 'favorites':[]}, status=200)

        favorites = []
        for favorite in queryset:
            product = { 'id': favorite.id_off,
                        'name': favorite.name,
                        'brands': favorite.brands,
                        'nutrition_grade': favorite.nutrition_grade,
                        'saturated_fat': favorite.satured_fat,
                        'fat': favorite.fat,
                        'sugar': favorite.sugar,
                        'salt': favorite.salt,
                        'categorie': favorite.categorie,
                        'img_url': favorite.img_url,
                        'off_url': favorite.url,
                        'url': request.build_absolute_uri(reverse('home:product', kwargs={'id':favorite.id_off}))
                    }
            favorites.append(product)
        return JsonResponse({'state': 'success', 'favorites':favorites}, status=200)
    except Profile.DoesNotExist:
        return JsonResponse({'state': 'error', 'reason': 'Incorrect Token / User Not Found'}, status=400)

def account(request):
    """Return Account View"""
    if request.user.is_authenticated:
        if request.method == 'POST' and 'emailchange' in request.POST:
            try:
                validate_email(request.POST.get('email'))
                request.user.email = request.POST.get('email')
                request.user.save()
            except Exception:
                pass
        return render(request, 'home/account.html')
    return render(request, 'home/notlogged.html', status=401)


def signup(request):
    """Return Signup View"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'home/signup.html', {'form': form})


def product(request, id):
    """Return Product View"""
    product = get_object_or_404(Product, id_off=id)
    context = {
        'product': product,
        'nutriscore': ['A', 'B', 'C', 'D', 'E']
    }
    return render(request, 'home/product.html', context)


def saveproduct(request, id):
    """Save or remove a product from a User's profile"""
    if request.user.is_authenticated:
        # Check if not already fav
        try:
            product = request.user.profile.favorites.get(id_off=id)
        except Product.DoesNotExist:
            try:
                product = Product.objects.get(id_off=id)
                request.user.profile.favorites.add(product)
                return JsonResponse({'state': 'success', 'action': 'added'}, status=200)
            except Product.DoesNotExist:
                return JsonResponse({'state': 'error', 'reason': 'Product does not exist', 'action': 'added'}, status=400)

        request.user.profile.favorites.remove(product)
        return JsonResponse({'state': 'success', 'action': 'removed'}, status=200)
    else:
        return JsonResponse({'state': 'error', 'reason': 'User not logged in', 'action': 'null'}, status=400)


def mentions(request):
    """Return Mentions View"""
    return render(request, 'home/mentions.html')
