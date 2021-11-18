from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registration_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 2:
            errors ['first_name'] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors ['last_name'] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):           
            errors['email'] = "Invalid email address!"
        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors ['email'] = "That email is already in use"
        if len(postData['password']) < 8:
            errors ['password'] = "Password should be at least 8 characters long"
        if postData['password'] != postData['pw_confirm']:
            errors['pw_confirm'] = "Password and PW_Confirm did not match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors ['email'] = "Email required"
        if len(postData['password']) < 8:
            errors ['password'] = "Password should be at least 8 characters long"
        if existing_user:
            log_user = existing_user[0]
            if bcrypt.checkpw(postData['password'].encode(),log_user.password.encode()) != True:
                errors['password'] = 'Email and password do not match'
        else:
            errors['password']= "Invalid login"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(max_length=70,blank=True, unique=True)
    password=models.CharField(max_length=12)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="post_comments", on_delete=models.CASCADE)

