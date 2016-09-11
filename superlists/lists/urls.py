from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /lists/
    url(r'^$', views.home_page, name='home'),
    url(r'^(.+)/$', views.view_list, name='view_list'),
    url(r'^new$', views.new_list, name='new_list'),
]
