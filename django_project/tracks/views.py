import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import Track
from artists.tasks import demorada


# Create your views here.
@login_required
@cache_page(60)
def track_view(request, title):
    # try:
    #    track = Track.object.get(title=title)
    # except Track.DoesNotExist:
    #    return Http404
    #import ipdb; ipdb.set_trace()
    track = get_object_or_404(Track, title=title)
    bio = track.artist.biography

    data = {
        'title': track.title,
        'order': track.order,
        'album': track.album.title,
        'artist': {
            'name': track.artist.name,
            'bio': bio,
        }
    }
    demorada.apply_async(countdown=5)
    json_data = json.dumps(data)
    #return HttpResponse(json_data, content_type='application/json')
    return render(request, 'track.html', {'track': track})

from rest_framework import viewsets
from serializers import TrackSerializer
class TrackViewSet(viewsets.ModelViewSet):
    model = Track
    queryset = Track.objects.all()
    serializer_class = TrackSerializer