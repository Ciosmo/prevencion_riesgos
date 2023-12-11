from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
# Models for  myforum

User = get_user_model()


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=40, blank=True)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    bio = HTMLField()
    points = models.IntegerField(default=0)
    profilePic = ResizedImageField(size=[50, 80], quality=100,upload_to="media/authors",default=None, null=True)
    
    
    def __str__(self):
        return self.fullname
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.fullname)
        super(Author, self).save(*args, **kwargs)
    
    

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(default="descripcion")
    
    class Meta:
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

        
    def get_url(self):
        return reverse("homeForumPosts", kwargs={
            "slug": self.slug
        })
        
    @property
    def numPosts(self):
        return Post.objects.filter(categories=self).count()

    @property
    def lastPosts(self):
        return Post.objects.filter(categories=self).latest("date")
    
    
class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:100]
       
    class Meta:
        verbose_name_plural = 'replies'
   
    
class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    replies  = models.ManyToManyField(Reply, blank=True)
    
    def __str__(self):
        return self.content[:100]
    
    
class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    categories = models.ManyToManyField(Category)
    date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    hitCountGeneric = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse("homeForumDetail", kwargs={
            "slug": self.slug
        })
    @property
    def numComments(self):
        return self.comments.count()
    @property
    def lastReply(self):
        return self.comments.latest("date")