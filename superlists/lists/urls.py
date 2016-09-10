from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /lists/
    url(r'^$', views.home_page, name='home'),
]
