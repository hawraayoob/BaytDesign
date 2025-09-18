from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import (
    Classification, Shop, Product, Budget, SelectedProduct,
    Cart, Wishlist, ProductReview, BudgetEstimate, UserProfile
)
from datetime import date, datetime
from decimal import Decimal

class ModelsTest(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create classification
        self.classification = Classification.objects.create(
            name='Furniture',
            description='Home furniture items'
        )
        
        # Create shop
        self.shop = Shop.objects.create(
            name='Test Furniture Shop',
            classification=self.classification,
            description='A test shop for furniture',
            phone='123-456-7890',
            email='test@shop.com',
            address='123 Test Street'
        )
        
        # Create products
        self.product1 = Product.objects.create(
            shop=self.shop,
            name='Test Chair',
            price=Decimal('99.99'),
            description='A comfortable chair',
            is_available=True
        )
        
        self.product2 = Product.objects.create(
            shop=self.shop,
            name='Test Table',
            price=Decimal('199.99'),
            description='A sturdy table',
            is_available=True
        )
        
        # Create budget
        self.budget = Budget.objects.create(
            user=self.user,
            total=Decimal('500.00')
        )
        
        # Create selected products for budget
        self.selected_product = SelectedProduct.objects.create(
            budget=self.budget,
            product=self.product1,
            quantity=2
        )
        
        # Create cart item
        self.cart_item = Cart.objects.create(
            user=self.user,
            product=self.product1,
            quantity=1
        )
        
        # Create wishlist item
        self.wishlist_item = Wishlist.objects.create(
            user=self.user,
            product=self.product2
        )
        
        # Create product review
        self.review = ProductReview.objects.create(
            user=self.user,
            product=self.product1,
            rating=4,
            comment='Great product!'
        )
        
        # Create budget estimate
        self.budget_estimate = BudgetEstimate.objects.create(
            user=self.user,
            estimated_cost=Decimal('1000.00'),
            details='Estimate for living room renovation'
        )
        
        # UserProfile should be automatically created by the signal

    def test_classification_creation(self):
        """Test that a classification can be created with expected attributes"""
        self.assertEqual(self.classification.name, 'Furniture')
        self.assertEqual(self.classification.slug, 'furniture')  
        self.assertEqual(self.classification.description, 'Home furniture items')
        
    def test_shop_creation(self):
        """Test that a shop can be created with expected attributes"""
        self.assertEqual(self.shop.name, 'Test Furniture Shop')
        self.assertEqual(self.shop.classification, self.classification)
        self.assertEqual(self.shop.phone, '123-456-7890')
        self.assertEqual(self.shop.email, 'test@shop.com')
        
    def test_product_creation(self):
        """Test that products can be created with expected attributes"""
        self.assertEqual(self.product1.name, 'Test Chair')
        self.assertEqual(self.product1.price, Decimal('99.99'))
        self.assertEqual(self.product1.shop, self.shop)
        self.assertTrue(self.product1.is_available)
        
    def test_budget_creation(self):
        """Test that a budget can be created with expected attributes"""
        self.assertEqual(self.budget.user, self.user)
        self.assertEqual(self.budget.total, Decimal('500.00'))
        
    def test_selected_product_creation(self):
        """Test that selected products can be added to a budget"""
        self.assertEqual(self.selected_product.budget, self.budget)
        self.assertEqual(self.selected_product.product, self.product1)
        self.assertEqual(self.selected_product.quantity, 2)
        
    def test_cart_creation(self):
        """Test that cart items can be created"""
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.product, self.product1)
        self.assertEqual(self.cart_item.quantity, 1)
        
    def test_wishlist_creation(self):
        """Test that wishlist items can be created"""
        self.assertEqual(self.wishlist_item.user, self.user)
        self.assertEqual(self.wishlist_item.product, self.product2)
        
    def test_product_review_creation(self):
        """Test that product reviews can be created"""
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.product, self.product1)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, 'Great product!')
        
    def test_budget_estimate_creation(self):
        """Test that budget estimates can be created"""
        self.assertEqual(self.budget_estimate.user, self.user)
        self.assertEqual(self.budget_estimate.estimated_cost, Decimal('1000.00'))
        
    def test_user_profile_creation(self):
        """Test that a user profile is automatically created for a new user"""
        self.assertTrue(hasattr(self.user, 'userprofile'))
        self.assertEqual(self.user.userprofile.user, self.user)
        
    def test_shop_product_relationship(self):
        """Test the relationship between shops and products"""
        shop_products = self.shop.product_set.all()
        self.assertEqual(shop_products.count(), 2)
        self.assertIn(self.product1, shop_products)
        self.assertIn(self.product2, shop_products)
        
    def test_budget_selected_products_relationship(self):
        """Test the relationship between budgets and selected products"""
        budget_products = self.budget.products.all()
        self.assertEqual(budget_products.count(), 1)
        self.assertEqual(budget_products.first(), self.selected_product)
        
    def test_product_reviews_relationship(self):
        """Test the relationship between products and reviews"""
        product_reviews = self.product1.reviews.all()
        self.assertEqual(product_reviews.count(), 1)
        self.assertEqual(product_reviews.first(), self.review)
        
    def test_classification_slug_generation(self):
        """Test that slugs are automatically generated for classifications"""
        test_classification = Classification.objects.create(
            name='Home Decor',
            description='Decorative items for home'
        )
        self.assertEqual(test_classification.slug, 'home-decor')
        
    def test_delete_user_cascades(self):
        """Test that deleting a user cascades to related objects"""
        user_id = self.user.id
        self.user.delete()
        
        # Check that related objects are deleted
        self.assertEqual(Budget.objects.filter(user_id=user_id).count(), 0)
        self.assertEqual(Cart.objects.filter(user_id=user_id).count(), 0)
        self.assertEqual(Wishlist.objects.filter(user_id=user_id).count(), 0)
        self.assertEqual(ProductReview.objects.filter(user_id=user_id).count(), 0)
        self.assertEqual(BudgetEstimate.objects.filter(user_id=user_id).count(), 0)
        self.assertEqual(UserProfile.objects.filter(user_id=user_id).count(), 0)
        
    def test_delete_shop_cascades_to_products(self):
        """Test that deleting a shop cascades to its products"""
        shop_id = self.shop.id
        product_ids = list(self.shop.product_set.values_list('id', flat=True))
        self.shop.delete()
        
        
        self.assertEqual(Product.objects.filter(id__in=product_ids).count(), 0)
        
    def test_delete_classification_cascades_to_shops(self):
        """Test that deleting a classification cascades to shops"""
        classification_id = self.classification.id
        shop_ids = list(self.classification.shop_set.values_list('id', flat=True))
        self.classification.delete()
        
        
        self.assertEqual(Shop.objects.filter(id__in=shop_ids).count(), 0)
