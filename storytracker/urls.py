from django.urls import path
from . import views

app_name = 'storytracker'

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('stories/<int:story_id>/', views.story_detail, name='story_detail'),
    path('stories/new/', views.new_story, name='new_story'),
    path('stories/<int:story_id>/edit/', views.edit_story, name='edit_story'),
    path('stories/<int:story_id>/updates/new/', views.new_update, name='new_update'),
    
    path('stories/<int:story_id>/delete/', views.delete_story, name='delete_story'),
    path('updates/<int:update_id>/delete/', views.delete_update, name='delete_update'),

]
