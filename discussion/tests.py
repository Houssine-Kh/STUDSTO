from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, UserActivity, PasswordReset, UserPrivacy, UserNotification, UserFollowRequest, Follow, Discussion, Message

class DiscussionModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='user1@example.com')
        self.user2 = User.objects.create(username='user2', email='user2@example.com')

    def test_str_representation(self):
        discussion = Discussion.objects.create(title='Test Discussion', user1=self.user1, user2=self.user2)
        self.assertEqual(str(discussion), 'Test Discussion')

class MessageModelTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create(username='sender', email='sender@example.com')
        self.recipient = User.objects.create(username='recipient', email='recipient@example.com')
        self.discussion = Discussion.objects.create(title='Test Discussion', user1=self.sender, user2=self.recipient)

    def test_str_representation(self):
        message = Message.objects.create(sender=self.sender, recipient=self.recipient, content='Test Content', discussion=self.discussion)
        self.assertEqual(str(message), f"From {self.sender.username} to {self.recipient.username} in {self.discussion.title} - Test Content")
