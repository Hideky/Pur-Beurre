import requests
import os
from .models import Product
from django.contrib.auth.models import User


API_URL = "https://fr.openfoodfacts.org/"


class OFFData:
    def __init__(self, search):
        self.search = search
        self.product = None

    def fetch(self, path):
        """Get dynamically data from the REST API of OpenFoodFacts"""
        path = "%s%s.json" % (API_URL, path)
        response = requests.get(path)
        return response.json()

    def fetch_m(self, path):
        """Get dynamically data from the REST API of OpenFoodFacts"""
        path = "%s%s" % (API_URL, path)
        response = requests.get(path)
        return response.json()

    def get_product(self):
        """Get data of a product"""
        try:
            query = Product.objects.filter(name__contains=self.search)
        except Product.DoesNotExist:
            query = None

        # If in DB
        if query:
            self.product = query[0]
            return query

        tag_country          = 'tagtype_0=countries&tag_contains_0=contains&tag_0=France&'        # From France
        tag_language         = 'tagtype_1=languages&tag_contains_1=contains&tag_1=fr&'            # French Name Translation Available
        tag_purshase_country = 'tagtype_2=purchase_places&tag_contains_2=contains&tag_2=France&'  # Purshasable in France
        tag_nutrition_grade  = 'tagtype_3=nutrition_grades&tag_contains_3=contains&tag_3=a&'      # Got a Nutrition grade equals to X
        tag_state            = 'tagtype_4=states&tag_contains_4=contains&tag_4=en%3Acomplete&'    # Product with every information completed
        url = 'https://fr.openfoodfacts.org/cgi/search.pl?{}json=1&action=process'
        url = url.format(tag_country + tag_language + tag_purshase_country + tag_nutrition_grade + tag_state)
        result = self.fetch("cgi/search.pl?{}search_terms2={}&page_size=1&page=1&action=process&json=1".format(tag_country + tag_language + tag_purshase_country + tag_state, self.search))['products']

        # If nothing found from OFF
        if not len(result):
            return None

        # If this product does not exist in DB, create it 
        if not Product.objects.filter(id_off=result[0]['id']):
            product = Product.objects.create(id_off=result[0]['id'],
                           name=result[0]['product_name'],
                         brands=result[0]['brands'],
                nutrition_grade=result[0]['nutrition_grade_fr'],
                    satured_fat=result[0]['nutriments']['saturated-fat_100g'],
                            fat=result[0]['nutriments']['fat_100g'],
                          sugar=result[0]['nutriments']['sugars_100g'],
                           salt=result[0]['nutriments']['salt_100g'],
                      categorie=max(result[0]['categories_prev_tags'], key=len),  # element['categories_prev_tags'][-1] for old method
                        img_url=result[0]['image_front_url'],
                            url=result[0]['url'])
            self.product = product
        else:
            self.product = Product.objects.get(id_off=result[0]['id'])
        return self.product

    def get_substitutes(self):
        """Get healthier products from a selected product"""
        query = Product.objects.filter(categorie=self.product.categorie)
        if len(query) >= 10:
            return query

        tag_country          = 'tagtype_0=countries&tag_contains_0=contains&tag_0=France&'        # From France
        tag_language         = 'tagtype_1=languages&tag_contains_1=contains&tag_1=fr&'            # French Name Translation Available
        tag_purshase_country = 'tagtype_2=purchase_places&tag_contains_2=contains&tag_2=France&'  # Purshasable in France
        tag_nutrition_grade  = 'tagtype_3=nutrition_grades&tag_contains_3=contains&tag_3=a&'      # Got a Nutrition grade equals to X
        tag_state            = 'tagtype_4=states&tag_contains_4=contains&tag_4=en%3Acomplete&'    # Product with every information completed
        url = "cgi/search.pl?tagtype_0=categories&tag_contains_0=contains&tag_0={}&{}page_size=250&page=1&action=process&json=1"
        result = self.fetch_m(url.format(self.product.categorie, tag_country + tag_language + tag_purshase_country + tag_state))
        
        products = list()

        for element in result['products']:
            healthy_test = 0
            # Data checking
            if not all(k in element for k in ("product_name", "brands", "id", "nutrition_grade_fr", "url", "categories_prev_tags")):
                continue
            if element['id'] == self.product.id_off:
                continue
            if not all(k in element['nutriments'] for k in ("fat_100g", "saturated-fat_100g", "sugars_100g", "salt_100g")):
                continue
            if not element['nutriments']['fat_100g']:
                continue
            if not element['nutriments']['saturated-fat_100g']:
                continue
            if not element['nutriments']['sugars_100g']:
                continue
            if not element['nutriments']['salt_100g']:
                continue

            # Healthy checking
            if float(element['nutriments']['fat_100g']) < float(self.product.fat):
                healthy_test += 1
            if float(element['nutriments']['saturated-fat_100g']) < float(self.product.satured_fat):
                healthy_test += 1
            if float(element['nutriments']['sugars_100g']) < float(self.product.sugar):
                healthy_test += 1
            if float(element['nutriments']['salt_100g']) < float(self.product.salt):
                healthy_test += 1
            if healthy_test < 3:
                continue

            # If this product does not exist in DB, create it
            if not Product.objects.filter(id_off=element['id']):
                new_product = Product.objects.create(id_off=element['id'],
                               name=element['product_name'],
                             brands=element['brands'],
                    nutrition_grade=element['nutrition_grade_fr'],
                        satured_fat=element['nutriments']['saturated-fat_100g'],
                                fat=element['nutriments']['fat_100g'],
                              sugar=element['nutriments']['sugars_100g'],
                               salt=element['nutriments']['salt_100g'],
                          categorie=max(element['categories_prev_tags'], key=len),
                            img_url=element['image_front_url'],
                                url=element['url'])
            else:
                new_product = Product.objects.get(id_off=element['id'])
            products.append(new_product)
        return products