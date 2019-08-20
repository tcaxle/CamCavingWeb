from django.urls import path
from . import views

urlpatterns = [
    path('Add/', views.BlogAdd.as_view(), name='BlogAdd'),
    path('Edit/<int:pk>', views.BlogEdit.as_view(), name='BlogEdit'),
    path('Delete/<int:pk>', views.BlogDelete.as_view(), name='BlogDelete'),
    path('ImageAdd/', views.ImageAdd.as_view(), name='ImageAdd'),
    path('ImageEdit/<int:pk>', views.ImageEdit.as_view(), name='ImageEdit'),
    path('ImageDelete/<int:pk>', views.ImageDelete.as_view(), name='ImageDelete'),
    path('', views.Blog.as_view(), name='Blog'),
]
