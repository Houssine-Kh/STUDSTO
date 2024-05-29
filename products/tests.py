from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product, ProductImage, Review, Like, Report
from accounts.models import UserProfile

class CategoryModelTest(TestCase):
    def test_str_representation(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(str(category), 'Test Category')

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.user_profile = UserProfile.objects.create(user=User.objects.create(username='testuser'))
        
    def test_str_representation(self):
        product = Product.objects.create(name='Test Product', description='Test Description', price=10.00, category=self.category, shared_by=self.user_profile)
        self.assertEqual(str(product), 'Test Product')

class ProductImageModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.00, category=self.category)

    def test_str_representation(self):
        product_image = ProductImage.objects.create(product=self.product, image='product_images/test_image.jpg')
        self.assertEqual(str(product_image), 'Test Product Image')

class ReviewModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.00, category=self.category)
        self.user = User.objects.create(username='testuser')

    def test_str_representation(self):
        review = Review.objects.create(user=self.user, product=self.product, content='Test Content')
        self.assertEqual(str(review), 'testuser - Test Product')

class LikeModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.00, category=self.category)
        self.user = User.objects.create(username='testuser')

    def test_str_representation(self):
        like = Like.objects.create(user=self.user, product=self.product)
        self.assertEqual(str(like), 'testuser likes Test Product')

class ReportModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.00, category=self.category)
        self.user = User.objects.create(username='testuser')

    def test_str_representation(self):
        report = Report.objects.create(user=self.user, product=self.product, reason='Test Reason')
        self.assertEqual(str(report), 'testuser reported Test Product')

