from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    birthdate = models.DateField(null=True, blank=True)
    TokenConfirmation = models.CharField(max_length=255, blank=True, null=True)
    isConfirmed = models.BooleanField(default=False)
    ProfilePic = models.ImageField(upload_to='user_images/',null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phoneNumber = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20)  # e.g., login, logout, etc.
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"
    
class UserPrivacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    private_profile = models.BooleanField(default=False)
    hide_followers = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Privacy"
    
class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
    
class UserFollowRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_requests_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_requests_received')
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user.username} to {self.to_user.username} - Follow Request"
    
class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile, related_name='followers_set', on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"

