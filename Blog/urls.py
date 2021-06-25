from django.urls import path
from . import views

urlpatterns = [
    path('Add/', views.BlogAdd.as_view(), name='BlogAdd'),
    path('Edit/<int:pk>', views.BlogEdit.as_view(), name='BlogEdit'),
    path('Delete/<int:pk>', views.BlogDelete.as_view(), name='BlogDelete'),
    # path('ImageAdd/', views.ImageAdd.as_view(), name='ImageAdd'), # upload image to cucc server
    path('Image/<int:pk>/Edit', views.ImageEdit.as_view(), name='ImageEdit'),
    path('Image/<int:pk>', views.ImageView.as_view(), name='ImageView'),
    # path('ImageDelete/<int:pk>', views.ImageDelete.as_view(), name='ImageDelete'),
    path('Album/Add', views.AlbumAdd.as_view(), name='AlbumAdd'),
    path('Album/<int:pk>', views.AlbumView, name='AlbumView'),
    path('Album/<int:pk>/SetCover', views.AlbumCoverUpdateSet, name='AlbumCoverUpdateSet'),
    path('Album/<int:pk>/UpdateImages', views.UpdateAlbumImages, name='UpdateAlbumImages'),
    path('Album/<int:pk>/UpdateDB', views.UpdateDBImages, name='UpdateBDImages'),
    path('Album/<int:pk>/Cover', views.AlbumCoverUpdate.as_view(), name='AlbumCoverUpdateView'),
    path('Album', views.AlbumList, name='Album'),
    path('Trip/Add', views.TripAdd.as_view(), name='TripAdd'),
    path('Trip/Stats', views.TripStats, name='TripStats'),
    path('Trip/Stats/<int:year>', views.TripStatsByYear, name='TripStatsByYear'),
    path('Trip/Stats/<int:year_start>/<int:year_end>', views.TripStatsByRange, name='TripStatsByRange'),
    path('Trip/<int:year>', views.TripListByYear, name='TripListByYear'),
    path('Trip/<int:year_start>/<int:year_end>', views.TripListByRange, name='TripListByRange'),
    path('Trip', views.TripList, name='Trip'),
    path('Author/<str:author>', views.BlogByAuthor.as_view(), name='ReportListByAuthor'), # TODO
    path('', views.Blog.as_view(), name='Blog'),
]
