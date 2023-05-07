from django.urls import path

from . import views, api


app_name = 'imageboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.registration, name='signup'),
    path('upload/', views.post_image, name='upload'),
    path('search/', views.SearchResultsView.as_view(), name='results'),
    path('<int:post_id>/', views.get_detail, name='view'),
    path('comment/<int:post_id>/',views.post_comment, name='comment'),
    path('tag/<int:post_id>/', views.add_tag, name='tag'),
    path('logout/', views.logout_view, name='logout'),
    path('api/tags', api.get_all_tagnames_sqlite3, name='apitags')
]