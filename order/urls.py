from django.urls import path
from . import views
app_name = 'order'
urlpatterns = [
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='add_to_cart')
]
