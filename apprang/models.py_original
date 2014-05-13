from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
"""Category provides model for categories."""
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Page(models.Model):
"""Page provides model for pages in Category model."""
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
""""UserProfile provides model for authentication, adds more fields"""

    """The user attribute is required to facilitate UserProfile to
       use django.contrib.auth.models.User by linking to models.Model.user."""
    user = models.OneToOneFields(User)

    """Additional attributes which are not included in User."""
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    """Overriding __unicode()__ method to return out something meaningful."""
    def __unicode__(self):
        return self.user.username
