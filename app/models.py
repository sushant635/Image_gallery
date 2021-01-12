from django.db import models
import uuid
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit 
# Create your models here.

class Album(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1024)
    thumb = ProcessedImageField(upload_to='album', processors=[ResizeToFit(300)], format='JPEG', options={'quality':90})
    tags = models.CharField(max_length=250)
    it_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50,unique=True)
    

    def __unicode__(self):
        return self.title

class AlbumImage(models.Model):
    image = ProcessedImageField(upload_to='album',processors=[ResizeToFit(1280)],format='JPEG',options={'quality':70})
    thumb = ProcessedImageField(upload_to='album',processors=[ResizeToFit(300)],format='JPEG',options={'quality':90})
    album = models.ForeignKey("app.Album",on_delete=models.CASCADE)
    alt = models.CharField(max_length=300,default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=30,default=uuid.uuid4,editable=False)

