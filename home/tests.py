from django.shortcuts import reverse
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from .models import Product
from .views import account, saveproduct, signup, favorites
from .OFFData import OFFData

class IndexPageTestCage(TestCase):
    """Test status code of Index Page"""
    def test_index_page_returns_200(self):
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)


class SearchPageTestCase(TestCase):
    """Test status code of Search Page with non-existing product"""
    def test_search_page_returns_200(self):
        response = self.client.get(reverse('home:search'), {'query': 'randomproductprobablynotexistinoff'})
        self.assertEqual(response.status_code, 200)

class ProductPageTestCase(TestCase):
    """Test status code of individual product page"""
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

    def test_product_page_returns_200(self):
        """Test status code of product page with existing product"""
        product_id = self.product.id_off
        response = self.client.get(reverse('home:product', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_product_page_returns_404(self):
        """Test status code of product page with non-existing product"""
        product_id = self.product.id_off + 1
        response = self.client.get(reverse('home:product', args=(product_id,)))
        self.assertEqual(response.status_code, 404)

class UserPagesTestCase(TestCase):
    """Test status code of all page with authenticating is required"""
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

    def test_account_page_returns_200(self):
        """Test status code of account page as logged user"""
        request = self.factory.get(reverse('home:account'))
        request.user = self.user

        response = account(request)
        self.assertEqual(response.status_code, 200)

    def test_account_page_returns_401(self):
        """Test status code of account page as anonymous user"""
        request = self.factory.get(reverse('home:account'))
        request.user = AnonymousUser()

        response = account(request)
        self.assertEqual(response.status_code, 401)

    def test_saveproduct_page_return_200(self):
        """Test status code of the save product API as logged user"""
        request = self.factory.get(reverse('home:saveproduct', args=(self.product.id_off,)))
        request.user = self.user
        response = saveproduct(request, id=self.product.id_off)
        self.assertEqual(response.status_code, 200)
        self.assertEqual( len(self.user.profile.favorites.all()), 1)

    def test_saveproduct_page_return_400(self):
        """Test status code of the save product API as anonymous user"""
        request = self.factory.get(reverse('home:saveproduct', args=(self.product.id_off,)))
        request.user = AnonymousUser()
        response = saveproduct(request, id=self.product.id_off)
        self.assertEqual(response.status_code, 400)

    def test_favorites_page_return_200(self):
        """Test status code of favorites page as logged user"""
        request = self.factory.get(reverse('home:favorites'))
        request.user = self.user
        response = favorites(request)
        self.assertEqual(response.status_code, 200)

    def test_favorites_page_return_400(self):
        """Test status code of favorites page as anonymous user"""
        request = self.factory.get(reverse('home:favorites'))
        request.user = AnonymousUser()
        response = favorites(request)
        self.assertEqual(response.status_code, 401)

class OFFDataTestCase(TestCase):
    """Test data return by OFFData in different case"""
    def test_offdata_return_result(self):
        """Test data return by OFFData with existing product"""
        offdata = OFFData('nutella')
        offdata.get_product()
        substitutes = offdata.get_substitutes()
        self.assertEqual(len(substitutes) > 1, True)

    def test_offdata_return_none(self):
        """Test data return by OFFData with a non-existing product"""
        offdata = OFFData('azertyuiopmlkjhgdswxcvbn')
        self.assertEqual(offdata.get_product(), None)