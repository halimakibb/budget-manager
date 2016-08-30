from django.shortcuts import render, render_to_response, redirect
from .models import Budget, User
from .forms import BudgetForm
import bcrypt
import datetime
# Create your views here.

def index(request):
	return render(request, template_name="task_scheduler/index.html")

def budget(request):
	if 'User' in request.session:
		user = User.objects.get(pk = request.session['User'])
		
		budgets = Budget.objects.filter(user_id = user.id)
		total = 0
		num = []
		for y in range(2016, datetime.datetime.now().year+1):
			num.append(y)

		for budget_item in budgets:
			total += budget_item.amount

		return render(request, template_name="task_scheduler/budget.html", context={'budgets': budgets,
																					'num': num,
																			    'total': total, })
	else:
		return redirect('/scheduler/login')

def newspending(request):
	if 'User' in request.session:
		user = User.objects.get(pk = request.session['User'])
		if (request.method == "POST"):
			form = BudgetForm(request.POST)
			if (form.is_valid):
				post = form.save(commit = False)
				post.user_id = user.id
				post.save()
			return redirect("/scheduler/budget")
		else:
			form = BudgetForm()
			return render(request, template_name="task_scheduler/newspending.html", context={'form': form,})
	else:
		return redirect('/scheduler/login')