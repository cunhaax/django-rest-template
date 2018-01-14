from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.loans, name='loans'),
    url(r'^(?P<loan_id>[0-9a-f-]+)$', views.detail, name='detail'),
    url(r'^(?P<loan_id>[0-9a-f-]+)/payments', views.payments, name='payment'),
    url(r'^(?P<loan_id>[0-9a-f-]+)/balance', views.balance, name='balance')
]
