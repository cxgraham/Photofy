from django.db import models
import re

# Create your models here.

# User Class
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'
            return errors
        email = postData['email']
        if User.objects.filter(email=email):
            errors['email'] = 'Email already in use'
            return errors
        if len(postData['password']) < 5: 
            errors['password'] = 'Password must be at least five characters'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Password  does not match'
        return errors

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.username


# Photo Class
class Photo(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField()
    private = models.BooleanField(default = True)
    user = models.ForeignKey(User, related_name = 'photos', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


