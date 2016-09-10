from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /lists/
    url(r'^$', views.home_page, name='home'),
    url(r'^the-only-list-in-the-world/$', views.view_list, name='view_list'),
]
