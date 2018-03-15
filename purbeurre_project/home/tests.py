from django.shortcuts import reverse
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from .models import Product
from .views import account, saveproduct, signup, favorites

# Index page
class IndexPageTestCage(TestCase):
    def test_index_page_returns_200(self):
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)


# Search page
class SearchPageTestCase(TestCase):
    def test_search_page_returns_200(self):
        response = self.client.get(reverse('home:search'), {'query': 'randomproductprobablynotexistinoff'})
        self.assertEqual(response.status_code, 200)

# Product page
class ProductPageTestCase(TestCase):
    def setUp(self):
        Product.objects.create(id_off=3274080005003,
                       name="Eau",
                     brands="CristEvianBadois",
            nutrition_grade="A",
                satured_fat=0,
                        fat=0.2,
                      sugar=0.3,
                       salt=0.4,
                  categorie="en:water",
                    img_url="https://static.openfoodfacts.org/images/products/327/408/000/5003/front_fr.220.400.jpg",
                        url="https://fr.openfoodfacts.org/produit/3274080005003/eau-de-source-cristaline"
            )
        self.product = Product.objects.get(id_off=3274080005003)

    # Product page with an existing product id
    def test_product_page_returns_200(self):
        product_id = self.product.id_off
        response = self.client.get(reverse('home:product', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    # Product page with a false product id
    def test_product_page_returns_404(self):
        product_id = self.product.id_off + 1
        response = self.client.get(reverse('home:product', args=(product_id,)))
        self.assertEqual(response.status_code, 404)

class UserPagesTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='TestUser', password='secretpwd')
        Product.objects.create(id_off=3274080005003,
                       name="Eau",
                     brands="CristEvianBadois",
            nutrition_grade="A",
                satured_fat=0,
                        fat=0.2,
                      sugar=0.3,
                       salt=0.4,
                  categorie="en:water",
                    img_url="https://static.openfoodfacts.org/images/products/327/408/000/5003/front_fr.220.400.jpg",
                        url="https://fr.openfoodfacts.org/produit/3274080005003/eau-de-source-cristaline"
            )
        self.product = Product.objects.get(id_off=3274080005003)

    # Account page as logged user
    def test_account_page_returns_200(self):
        request = self.factory.get(reverse('home:account'))
        request.user = self.user

        response = account(request)
        self.assertEqual(response.status_code, 200)

    # Account page as anonymous user
    def test_account_page_returns_401(self):
        request = self.factory.get(reverse('home:account'))
        request.user = AnonymousUser()

        response = account(request)
        self.assertEqual(response.status_code, 401)

    # Save Product API as logged user
    def test_saveproduct_page_return_200(self):
        request = self.factory.get(reverse('home:saveproduct', args=(self.product.id_off,)))
        request.user = self.user
        response = saveproduct(request, id=self.product.id_off)
        self.assertEqual(response.status_code, 200)
        self.assertEqual( len(self.user.profile.favorites.all()), 1)

    # Save Product API as anonymous user
    def test_saveproduct_page_return_400(self):
        request = self.factory.get(reverse('home:saveproduct', args=(self.product.id_off,)))
        request.user = AnonymousUser()
        response = saveproduct(request, id=self.product.id_off)
        self.assertEqual(response.status_code, 400)

    # Favorites Page as logged user
    def test_favorites_page_return_200(self):
        request = self.factory.get(reverse('home:favorites'))
        request.user = self.user
        response = favorites(request)
        self.assertEqual(response.status_code, 200)

    # Favorites Page as anonymous user
    def test_favorites_page_return_400(self):
        request = self.factory.get(reverse('home:favorites'))
        request.user = AnonymousUser()
        response = favorites(request)
        self.assertEqual(response.status_code, 401)