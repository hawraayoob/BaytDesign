from django.contrib import admin
from .models import (
    Classification, Shop, Product,
    Budget, SelectedProduct, Cart,
    Wishlist, ProductReview, BudgetEstimate,
    UserProfile
)

# Classification admin
@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}  # auto-generate slug

# Shop admin
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "classification", "phone", "email")
    search_fields = ("name", "classification__name")
    list_filter = ("classification",)

# Product admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "price", "is_available")
    search_fields = ("name", "shop__name")
    list_filter = ("shop", "is_available")

# Register other models quickly
admin.site.register(Budget)
admin.site.register(SelectedProduct)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(ProductReview)
admin.site.register(BudgetEstimate)
admin.site.register(UserProfile)
