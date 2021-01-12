from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from app.models import Album, AlbumImage

def index(request):
    photo = Album.objects.filter(it_visible=True).order_by('-created')
    paginator = Paginator(photo,10)

    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages) 

    return render(request,'app/index.html',{'albums':photo})

class AlbumDetail(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        context = super(AlbumDetail,self).get_context_data(**kwargs)
        context['images'] = AlbumImage.objects.filter(album=self.object.id)
        return context


def handler404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)
