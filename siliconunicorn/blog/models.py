from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import random


# Custom User for future customization
class UnicornUser(AbstractUser):
    def __str__(self):
        return self.username


#Blog Post Class
class Post(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(UnicornUser, related_name='post_author', on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    likes = models.ManyToManyField(UnicornUser, related_name='post_likes', blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date_published"]

    # def save(self, *args, **kwargs):
    #     if self.pk is not None:
    #         self.like_count = self.likes.count()
    #         self.comment_count = self.post_comments.filter(active=True).count()
    #     super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/%s" % self.slug

    @property
    def get_next_post_url(self):
        next = self.pk + 1
        total = Post.objects.latest('id').id
        while next <= total:
            try:
                p = Post.objects.get(pk=next)
                if (p.active == True):
                    return '/blog/' + p.slug
            except Post.DoesNotExist:
                pass
            next += 1
        return '/'

    @property
    def get_prev_post_url(self):
        prev = self.pk - 1
        while prev >= 0:
            try:
                p = Post.objects.get(pk=prev)
                if (p and p.active == True):
                    return '/blog/' + p.slug
            except Post.DoesNotExist:
                pass
            prev -= 1
        return '/'

    def get_like_count(self):
        return self.like_count

    def get_comment_count(self):
        return self.post_comments.filter(active=True).count()

#Comment Class
class Comment(models.Model):
    def __str__(self):
        return self.content

    display_author = models.CharField(max_length=200, default="anonymous coward")
    author = models.ForeignKey(UnicornUser, related_name='comment_author', null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    content = models.TextField()
    parent_post = models.ForeignKey('Post', related_name='post_comments', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    likes = models.ManyToManyField(UnicornUser, related_name='comment_likes', blank=True)
    like_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.like_count = self.likes.count()
        super(Comment, self).save(*args, **kwargs)

    def get_like_count(self):
        # return self.like_count
        return self.likes.count()


    @property
    def is_edited(self):
        return self.last_edited.replace(microsecond=0) > self.timestamp.replace(microsecond=0)
