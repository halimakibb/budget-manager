from django.conf.urls import url
from . import views
from .views.login_and_registration import views as loginviews
from .views.budget import views as budgetviews

urlpatterns = [
	
	url(r'^index$', budgetviews.index, name='index'),
	url(r'^budget$', budgetviews.get_budget, name='budget'),
	url(r'^editbudget/(?P<budget_pk>\d+)/(?P<page_number>\d+)$', budgetviews.edit_budget, name='editbudget'),
	url(r'^deletebudget/(?P<budget_pk>\d+)/(?P<page_number>\d+)$', budgetviews.delete_budget, name='deletebudget'),
	url(r'^newspending$', budgetviews.add_budget, name='newspending'),
	url(r'^register$', loginviews.register, name='register'),
	url(r'^login$', loginviews.login, name='login'),
	url(r'^logout$', loginviews.logout, name='logout'),
	
]




