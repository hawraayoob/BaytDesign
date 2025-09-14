from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Classification, Shop, Product, Budget, SelectedProduct, Cart, Wishlist, ProductReview, BudgetEstimate



# -----------------------
# AUTH VIEWS
# -----------------------
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# -----------------------
# HOME & CLASSIFICATION VIEWS
# -----------------------
def home_view(request):
    classifications = Classification.objects.all()
    return render(request, 'home.html', {'classifications': classifications})

@login_required
def classification_stores_view(request, slug):
    classification = get_object_or_404(Classification, slug=slug)
    shops = Shop.objects.filter(classification=classification)
    return render(request, 'classification_stores.html', {
        'classification': classification,
        'shops': shops
    })

# -----------------------
# SHOP & PRODUCT VIEWS
# -----------------------
@login_required
def shop_products_view(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    products = Product.objects.filter(shop=shop)
    return render(request, 'shop_products.html', {
        'shop': shop,
        'products': products
    })

# -----------------------
# ADMIN VIEWS
# -----------------------
@staff_member_required
def add_shop_view(request, classification_id):
    classification = get_object_or_404(Classification, id=classification_id)
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        image = request.FILES.get('image')
        
        shop = Shop.objects.create(
            name=name,
            description=description,
            address=address,
            phone=phone,
            email=email,
            classification=classification
        )
        
        if image:
            shop.image = image
            shop.save()
            
        return redirect('classification_stores', slug=classification.slug)
    return render(request, 'add_shop.html', {'classification': classification})

@staff_member_required
def add_product_view(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        is_available = request.POST.get('is_available') == 'true'
        image = request.FILES.get('image')
        
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            is_available=is_available,
            shop=shop
        )
        
        if image:
            product.image = image
            product.save()
            
        return redirect('shop_products', shop_id=shop.id)
    return render(request, 'add_product.html', {'shop': shop})

# -----------------------
# BUDGET VIEWS
# -----------------------
@login_required
def budget_view(request):
    budget, created = Budget.objects.get_or_create(user=request.user)
    selected_products = SelectedProduct.objects.filter(user=request.user)
    total_spent = sum([p.total_price for p in selected_products])

    if request.method == "POST":
        new_budget = request.POST.get('budget')
        if new_budget:
            budget.total_amount = float(new_budget)
            budget.save()
            return redirect('budget')

    # Calculate budget-related values
    remaining_budget = budget.total_amount - total_spent
    budget_percentage = (total_spent / budget.total_amount * 100) if budget.total_amount > 0 else 0
    is_over_budget = total_spent > budget.total_amount
    is_near_budget = total_spent > (budget.total_amount * 0.9) if budget.total_amount > 0 else False

    return render(request, 'budget.html', {
        'budget': budget.total_amount,
        'selected_products': selected_products,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'budget_percentage': budget_percentage,
        'is_over_budget': is_over_budget,
        'is_near_budget': is_near_budget,
    })

@login_required
def add_to_budget_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is already in user's budget
    existing_selection = SelectedProduct.objects.filter(user=request.user, product=product).first()
    
    if existing_selection:
        existing_selection.quantity += 1
        existing_selection.save()
    else:
        SelectedProduct.objects.create(user=request.user, product=product)
    
    return redirect('budget')

@login_required
def remove_from_budget_view(request, selected_product_id):
    selected_product = get_object_or_404(SelectedProduct, id=selected_product_id, user=request.user)
    selected_product.delete()
    return redirect('budget')

@login_required
def update_quantity_view(request, selected_product_id):
    selected_product = get_object_or_404(SelectedProduct, id=selected_product_id, user=request.user)
    new_quantity = int(request.POST.get('quantity', 1))
    
    if new_quantity > 0:
        selected_product.quantity = new_quantity
        selected_product.save()
    else:
        selected_product.delete()
    
    return redirect('budget')


# -----------------------
# CART VIEWS (My Cart)
# -----------------------
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum([item.total_price for item in cart_items])
    
    # Get user's budget
    budget, created = Budget.objects.get_or_create(user=request.user)
    
    # Calculate budget-related values
    is_over_budget = total_price > budget.total_amount if budget.total_amount > 0 else False
    over_budget_amount = total_price - budget.total_amount if is_over_budget else 0
    budget_percentage = (total_price / budget.total_amount * 100) if budget.total_amount > 0 else 0
    is_near_budget = total_price > (budget.total_amount * 0.9) if budget.total_amount > 0 else False
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'budget': budget.total_amount,
        'is_over_budget': is_over_budget,
        'over_budget_amount': over_budget_amount,
        'budget_percentage': budget_percentage,
        'is_near_budget': is_near_budget,
    })

@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is already in cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart')

@login_required
def remove_from_cart_view(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')

@login_required
def update_cart_quantity_view(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    new_quantity = int(request.POST.get('quantity', 1))
    
    if new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')


# -----------------------
# WISHLIST VIEWS (My List)
# -----------------------
@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if already in wishlist
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to your list!')
    else:
        messages.info(request, f'{product.name} is already in your list!')
    
    return redirect('wishlist')

@login_required
def remove_from_wishlist_view(request, wishlist_item_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_item_id, user=request.user)
    wishlist_item.delete()
    messages.success(request, 'Item removed from your list!')
    return redirect('wishlist')

@login_required
def mark_as_purchased_view(request, wishlist_item_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_item_id, user=request.user)
    wishlist_item.is_purchased = not wishlist_item.is_purchased
    wishlist_item.save()
    
    status = "marked as purchased" if wishlist_item.is_purchased else "marked as not purchased"
    messages.success(request, f'{wishlist_item.product.name} {status}!')
    return redirect('wishlist')


# -----------------------
# REVIEW VIEWS
# -----------------------
@login_required
def add_review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        review_text = request.POST.get('review_text', '')
        
        # Check if user already reviewed this product
        existing_review = ProductReview.objects.filter(user=request.user, product=product).first()
        
        if existing_review:
            existing_review.rating = rating
            existing_review.review_text = review_text
            existing_review.save()
            messages.success(request, 'Review updated!')
        else:
            ProductReview.objects.create(
                user=request.user,
                product=product,
                rating=rating,
                review_text=review_text
            )
            messages.success(request, 'Review added!')
        
        return redirect('shop_products', shop_id=product.shop.id)
    
    return render(request, 'add_review.html', {'product': product})

@login_required
def product_reviews_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = ProductReview.objects.filter(product=product).order_by('-created_date')
    
    # Calculate average rating
    if reviews:
        avg_rating = sum([review.rating for review in reviews]) / len(reviews)
    else:
        avg_rating = 0
    
    return render(request, 'product_reviews.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })
