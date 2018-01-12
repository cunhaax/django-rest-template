from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.loans, name='loans-list'),
    # url(r'^(?P<loan_id>[0-9]+)', views.get_loan, name='loan-detail')
]
