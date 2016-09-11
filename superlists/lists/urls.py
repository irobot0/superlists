from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /lists/
    # url(r'^$', views.home_page, name='home'),

    # ex: /lists/1/
    url(r'^(\d+)/$', views.view_list, name='view_list'),

    # ex: /lists/1/add_item
    url(r'^(\d+)/add_item', views.add_item, name='add_item'),

    # ex: /lists/new
    url(r'^new$', views.new_list, name='new_list'),
]
