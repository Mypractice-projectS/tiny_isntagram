from django.db import models
from accounts.models import User




#    Post

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField()
    image = models.ImageField(upload_to='static/posts/')
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # share = models.BooleanField(default=False)

    def __str__(self):
        return (f'{self.caption}, {self.user}, {self.is_active},'
                f' {self.is_public}, {self.created_at}, {self.updated_at}')





#  Comment

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.text}, {self.user}, {self.created_at}'


#   Like

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT,related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}, {self.post}, {self.created_at}'

class follow(models.Model):
    follow_from = models.ForeignKey(User, on_delete=models.PROTECT, related_name='friend_follow_from')
    follow_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='friend_follow_to')
    is_accepted = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('follow_from', 'follow_to')