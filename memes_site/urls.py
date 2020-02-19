from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('page/<int:page_number>', views.index_page, name='index_page'),
    path('image/<int:image_id>/', views.image_view, name='image'),
    path('image/upload/', views.image_upload_view, name='image_upload'),
    path('image/delete/', views.image_delete, name='image_delete'),
    path('image/vote_up/<int:image_id>/', views.image_vote_up, name='vote_up'),
    path('image/vote_down/<int:image_id>/', views.image_vote_down, name='vote_down'),
    path('comment/<str:vote_type>/<int:comment_id>/', views.comment_vote, name='comment_vote_up'),
    path('create_comment/<int:image_id>/', views.create_comment, name='create_comment'),
    path('comment/delete/', views.delete_comment, name='delete_comment'),
    path('fresh/page/<int:page_number>', views.fresh_view, name='fresh'),
    path('fresh/', views.fresh_view, name='fresh_page'),
    path('user/<str:username>/', views.user_view, name='user_memes')
]
app_name = 'memes'
