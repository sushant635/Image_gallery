import os
import uuid
import zipfile
from django.conf import settings
from datetime import datetime
from zipfile import ZipFile
from django.contrib import admin
from django.core.files.base import ContentFile
from PIL import Image
from app.models import Album, AlbumImage
from app.forms import AlbumForm


@admin.register(Album)
class AblumModelAdmin(admin.ModelAdmin):
    form = AlbumForm
    prepopulated_fileds = {'slug':('title',)}
    photo_display = ('title','thumb')
    photo_filter = ('cretaed',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            ablum = form.save(commit=False)
            ablum.modified = datetime.now()
            ablum.save()

            if form.cleaned_data['zip'] != None :
                zip = zipfile.ZipFile(form.cleaned_data['zip'])
                for filename in sorted(zip.namelist()):
                    file_name = os.path.basename(filename)
                    if not file_name:
                        continue

                    data = zip.read(filename)
                    contentfile = ContentFile(data)

                    img = AlbumImage()
                    img.album = ablum
                    img.alt = filename
                    filename = '{0}{1}.jpg'.format(ablum.slug, str(uuid.uuid4())[-13:])
                    img.image.save(filename,contentfile)

                    filepath = '{0}/ablum/{1}'.format(settings.MEDIA_ROOT,filename)
                    with Image.open(filepath) as i :
                        img.width, img.height = i.size

                    img.thumb.save('thumb-{0}'.format(filename),contentfile)
                    img.save()
                zip.close()
            super(AblumModelAdmin,self).save_model(request,obj,form,change)

@admin.register(AlbumImage)
class AblumImageModelAdmin(admin.ModelAdmin):
    list_display = ('alt', 'album')
    list_filter = ('album', 'created')


                
