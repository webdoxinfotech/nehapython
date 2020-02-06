from . import views
from django.urls import path,include
from .resources import PostResource

post_resource = PostResource()



urlpatterns = [
	path('', views.index, name='post_list'),
	path('about', views.about),
	path('post_detail/<int:pk>', views.postDetail, name='post_detail'),
	path('post_new', views.postCreate, name='post_new'),
	path('neha', views.nehapage),
	path('post_edit/<int:pk>/edit', views.post_edit, name='post_edit'),
	path('signup', views.signup, name='signup'),


	path('api/', include(post_resource.urls)),

]