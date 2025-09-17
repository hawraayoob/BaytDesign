from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='accounts_login'),

    # Home & classifications
    path('', views.home_view, name='home'),
    path('classification/<slug:slug>/', views.classification_stores_view, name='classification_stores'),

    # Shop & products
    path('shop/<int:shop_id>/', views.shop_products_view, name='shop_products'),

    # Admin add shop/product
    path('add-shop/<int:classification_id>/', views.add_shop_view, name='add_shop'),
    path('add-product/<int:shop_id>/', views.add_product_view, name='add_product'),

    # Budget
    path('budget/', views.budget_view, name='budget'),
    path('add-to-budget/<int:product_id>/', views.add_to_budget_view, name='add_to_budget'),
    path('remove-from-budget/<int:selected_product_id>/', views.remove_from_budget_view, name='remove_from_budget'),
    path('update-quantity/<int:selected_product_id>/', views.update_quantity_view, name='update_quantity'),

    # Cart (My Cart)
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('update-cart-quantity/<int:cart_item_id>/', views.update_cart_quantity_view, name='update_cart_quantity'),

    # Wishlist (My List)
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist_view, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist_view, name='remove_from_wishlist'),
    path('mark-as-purchased/<int:wishlist_item_id>/', views.mark_as_purchased_view, name='mark_as_purchased'),

    # Reviews
    path('add-review/<int:product_id>/', views.add_review_view, name='add_review'),
    path('product-reviews/<int:product_id>/', views.product_reviews_view, name='product_reviews'),
    path('edit-review/<int:review_id>/', views.edit_review_view, name='edit_review'),   # ✅ Added
    path('delete-review/<int:review_id>/', views.delete_review_view, name='delete_review'),  # ✅ Added

    # About page
    path('about/', views.about_view, name='about'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('update-profile/', views.update_profile_view, name='update_profile'),
    path('change-password/', views.change_password_view, name='change_password'),
]