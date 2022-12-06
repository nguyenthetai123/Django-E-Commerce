from django.urls import reverse, path
from . import views
urlpatterns = [
      path('addcomment/<int:id>', views.addcomment, name='addcomment'),
]
