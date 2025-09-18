from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Classification, Shop, Product, Budget, SelectedProduct, Cart, Wishlist, ProductReview, BudgetEstimate, UserProfile


def is_admin(user):
    return user.is_superuser


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



@login_required
def shop_products_view(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    products = Product.objects.filter(shop=shop)
    return render(request, 'shop_products.html', {
        'shop': shop,
        'products': products
    })



@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
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



@login_required
def budget_view(request):
    from decimal import Decimal, InvalidOperation
    

    budget = None
    

    try:

        budget = Budget.objects.filter(user=request.user).first()
        if not budget:

            budget = Budget.objects.create(user=request.user, total=Decimal('0'))
            budget.save()

        Decimal(str(budget.total))
    except (InvalidOperation, ValueError):

        if budget:
            budget.total = Decimal('0')
            budget.save()
        else:
            budget = Budget.objects.create(user=request.user, total=Decimal('0'))
            budget.save()
    

    if request.method == "POST":
        new_budget = request.POST.get('budget')
        if new_budget:
            try:

                new_budget_decimal = Decimal(new_budget.strip())
                budget.total = new_budget_decimal
                budget.save()

                from django.db import transaction
                transaction.commit()
                messages.success(request, "Budget updated successfully!")

            except (InvalidOperation, ValueError) as e:

                messages.error(request, f"Invalid budget amount. Please enter a valid number.")

    
    selected_products = SelectedProduct.objects.filter(budget=budget, user=request.user)
    

    for product in selected_products:
        try:
            product.total_price = product.product.price * product.quantity
        except (InvalidOperation, TypeError):

            product.total_price = Decimal('0')
    

    cart_items = Cart.objects.filter(user=request.user)
    cart_total = Decimal('0')
    for item in cart_items:
        try:
            cart_total += item.product.price * item.quantity
        except (InvalidOperation, TypeError):

            pass
    

    budget_products_total = Decimal('0')
    for p in selected_products:
        try:
            budget_products_total += p.total_price
        except (InvalidOperation, TypeError):

            pass
    
    total_spent = budget_products_total + cart_total

    try:
        remaining_budget = budget.total - total_spent
    except (InvalidOperation, TypeError):
        remaining_budget = Decimal('0')
        
    try:
        if budget.total > 0:
            budget_percentage = (total_spent / budget.total * Decimal('100'))

        else:
            budget_percentage = Decimal('0')
    except (InvalidOperation, TypeError, ZeroDivisionError):
        budget_percentage = Decimal('0')
        
    try:

        is_over_budget = total_spent > budget.total
    except (InvalidOperation, TypeError):
        is_over_budget = False
        
    try:
        is_near_budget = total_spent > (budget.total * Decimal('0.9')) if budget.total > 0 else False
    except (InvalidOperation, TypeError):
        is_near_budget = False

    return render(request, 'budget.html', {
        'budget': budget,
        'selected_products': selected_products,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'budget_percentage': budget_percentage,
        'is_over_budget': is_over_budget,
        'is_near_budget': is_near_budget,
        'budget_created_at': budget.created_at
    })

@login_required
def add_to_budget_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    budget, created = Budget.objects.get_or_create(user=request.user)
    
    existing_selection = SelectedProduct.objects.filter(product=product, budget=budget, user=request.user).first()
    
    if existing_selection:
        existing_selection.quantity += 1
        existing_selection.save()
    else:
        SelectedProduct.objects.create(product=product, budget=budget, user=request.user)
    

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('budget')

@login_required
def remove_from_budget_view(request, selected_product_id):
    budget = Budget.objects.get_or_create(user=request.user)[0]
    selected_product = get_object_or_404(SelectedProduct, id=selected_product_id, user=request.user, budget=budget)
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


@login_required
def cart_view(request):
    from decimal import Decimal, InvalidOperation
    
    cart_items = Cart.objects.filter(user=request.user)

    total_price = Decimal('0')
    for item in cart_items:
        try:
            total_price += item.product.price * item.quantity
        except (InvalidOperation, TypeError):

            pass
    

    budget = None
    

    try:

        budget = Budget.objects.filter(user=request.user).first()
        if not budget:
            budget = Budget.objects.create(user=request.user, total=Decimal('0'))

        Decimal(str(budget.total))
    except (InvalidOperation, ValueError):

        if budget:
            budget.total = Decimal('0')
            budget.save()
        else:
            budget = Budget.objects.create(user=request.user, total=Decimal('0'))
    
    try:
        is_over_budget = total_price > budget.total if budget.total > 0 else False
        over_budget_amount = total_price - budget.total if is_over_budget else Decimal('0')
        budget_percentage = (total_price / budget.total * Decimal('100')) if budget.total > 0 else Decimal('0')
        is_near_budget = total_price > (budget.total * Decimal('0.9')) if budget.total > 0 else False
    except (InvalidOperation, TypeError, ZeroDivisionError):
        is_over_budget = False
        over_budget_amount = Decimal('0')
        budget_percentage = Decimal('0')
        is_near_budget = False
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'budget': budget.total,
        'is_over_budget': is_over_budget,
        'over_budget_amount': over_budget_amount,
        'budget_percentage': budget_percentage,
        'is_near_budget': is_near_budget,
    })

@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('shop_products', shop_id=product.shop.id)

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


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f'{product.name} added to your list!')
    else:
        messages.info(request, f'{product.name} is already in your list!')
    

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('shop_products', shop_id=product.shop.id)

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


@login_required
def add_review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        review_text = request.POST.get('comment', '')
        
        existing_review = ProductReview.objects.filter(user=request.user, product=product).first()
        
        if existing_review:
            existing_review.rating = rating
            existing_review.comment = review_text
            existing_review.save()
            messages.success(request, 'Review updated!')
        else:
            ProductReview.objects.create(user=request.user, product=product, rating=rating, comment=review_text)
            messages.success(request, 'Review added!')
        
        return redirect('shop_products', shop_id=product.shop.id)
    
    return render(request, 'add_review.html', {'product': product})

@login_required
def product_reviews_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = ProductReview.objects.filter(product=product).order_by('-created_at')
    avg_rating = sum([review.rating for review in reviews]) / len(reviews) if reviews else 0
    
    return render(request, 'product_reviews.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })


def about_view(request):
    return render(request, 'about.html')


@login_required
def profile_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    user_reviews = ProductReview.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {
        'wishlist_items': wishlist_items,
        'user_reviews': user_reviews
    })

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        profile_picture = request.FILES.get('profile_picture')
        

        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        

        if username != request.user.username and User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('profile')
        

        if profile_picture:
            user_profile.profile_picture = profile_picture
            user_profile.save()
        

        request.user.username = username
        request.user.first_name = first_name
        request.user.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    
    return redirect('profile')

@login_required
def edit_review_view(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id, user=request.user)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '')
        
        review.rating = rating
        review.comment = comment
        review.save()
        messages.success(request, 'Review updated successfully!')
        return redirect('profile')
    
    return render(request, 'edit_review.html', {'review': review})

@login_required
def delete_review_view(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('profile')

@login_required
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        

        if not request.user.check_password(old_password):
            messages.error(request, 'Your current password is incorrect.')
            return redirect('profile')
        

        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('profile')
        

        request.user.set_password(new_password1)
        request.user.save()
        

        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Your password has been changed successfully.')
        return redirect('profile')
    
    return redirect('profile')
