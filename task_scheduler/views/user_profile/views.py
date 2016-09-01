from django.shortcuts import render, render_to_response, redirect
from task_scheduler.models import Budget, User, BudgetType, DebitOrCredit
from task_scheduler.forms import BudgetForm
import bcrypt
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from _datetime import timedelta, date
import locale

def profile(request):
	if request.method == 'GET':
		if 'User' in request.session:
			user = User.objects.get(pk = request.session['User'])
			return render(request, template_name="task_scheduler/profilepage.html", context={'user' : user,
																					  })
		else:
			return redirect("/scheduler/budget/login")
	else:
		if 'User' in request.session:
			maketrans = str.maketrans
			user = User.objects.get(pk = request.session['User'])
			user.first_name = request.POST.get('id_first_name')
			user.last_name = request.POST.get('id_last_name')
			
			monthly_budget = request.POST.get('id_monthly_budget')
			monthly_budget = monthly_budget.translate(maketrans(',.', '.,'))
			monthly_budget = monthly_budget.replace(",", "")
			monthly_budget = monthly_budget.replace("Rp", "")

			user.monthly_budget_target = monthly_budget

			user.save()
			return redirect("/scheduler/budget/profile")
		else:
			return redirect("/scheduler/budget/login")