from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Product, Profile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brands', 'categorie', 'url')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'brands')
    list_per_page = 50
    readonly_fields = ['name', 'brands', 'categorie', 'nutrition_grade', 'satured_fat', 'fat', 'sugar', 'salt', 'img_url', 'url', 'id_off']

    def has_add_permission(self, request):
        return False

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('api_token', 'favorites_link')
    readonly_fields = ['api_token', 'favorites_link']
    def favorites_link(self, profile):
        path = "admin:home_product_change"
        links = ["<li><a href='{}'>{}</a></li>".format(reverse(path, args=(o.id,)), o.name) for o in profile.favorites.all()]
        return mark_safe("\n".join(links))

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = UserAdmin.list_display + ('favorites',)

    def favorites(self, user):
        return len(user.profile.favorites.all())
    favorites.short_description = "Nombre de favoris"

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)