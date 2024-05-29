from django.test import TestCase

from django.contrib.auth.models import User
from .models import UserProfile, UserActivity, PasswordReset, UserPrivacy, UserNotification, UserFollowRequest, Follow

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_str_representation(self):
        profile = UserProfile.objects.create(user=self.user, firstName='John', lastName='Doe')
        self.assertEqual(str(profile), 'John Doe')

class UserActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_str_representation(self):
        activity = UserActivity.objects.create(user=self.user, activity_type='login')
        self.assertEqual(str(activity), 'testuser - login')

class PasswordResetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_str_representation(self):
        reset = PasswordReset.objects.create(user=self.user, token='abc123')
        self.assertEqual(str(reset), 'testuser - abc123')

class UserPrivacyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_str_representation(self):
        privacy = UserPrivacy.objects.create(user=self.user, private_profile=True, hide_followers=True)
        self.assertEqual(str(privacy), 'testuser - Privacy')

class UserNotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_str_representation(self):
        notification = UserNotification.objects.create(user=self.user, message='Hello, world!')
        self.assertEqual(str(notification), 'testuser - Hello, world!')

class UserFollowRequestModelTest(TestCase):
    def setUp(self):
        self.from_user = User.objects.create(username='from_user', email='from@example.com')
        self.to_user = User.objects.create(username='to_user', email='to@example.com')

    def test_str_representation(self):
        follow_request = UserFollowRequest.objects.create(from_user=self.from_user, to_user=self.to_user)
        self.assertEqual(str(follow_request), 'from_user to to_user - Follow Request')

class FollowModelTest(TestCase):
    def setUp(self):
        self.follower = User.objects.create(username='follower', email='follower@example.com')
        self.following = User.objects.create(username='following', email='following@example.com')
        self.follower_profile = UserProfile.objects.create(user=self.follower)
        self.following_profile = UserProfile.objects.create(user=self.following)

    def test_str_representation(self):
        follow = Follow.objects.create(follower=self.follower_profile, following=self.following_profile)
        self.assertEqual(str(follow), 'follower follows following')
