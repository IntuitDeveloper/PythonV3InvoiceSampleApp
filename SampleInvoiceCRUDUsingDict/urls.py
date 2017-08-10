from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/?$', views.index, name='indexInvoiceDict'),
    url(r'^(?i)/create/?$', views.create, name='create'),
    url(r'^(?i)/update/?$', views.update, name='update'),
    url(r'^(?i)/read/?$', views.read, name='read'),
    url(r'^(?i)/delete/?$', views.delete, name='delete'),
    url(r'^(?i)/query/?$', views.query, name='query'),

]