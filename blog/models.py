from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)



    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # creating method for approved comments only to display for home page.we say this function a method because its the part of a class.
    def approved_comments(self):
        return self.comments.filter(approved=True)
    # create a string representation,rather then object form.good practice too.
    def __str__(self):
        # return f"({self.title} by {self.author})"
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments') #that related name is used when we want to access our all comments of a specific post.
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()


    def __str__(self):
        return self.text
    

