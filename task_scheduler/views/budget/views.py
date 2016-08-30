from django.shortcuts import render, render_to_response, redirect
from task_scheduler.models import Budget, User, BudgetType, DebitOrCredit
from task_scheduler.forms import BudgetForm
import bcrypt
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from _datetime import timedelta, date
import locale

def index(request):
	return render(request, template_name="task_scheduler/index.html")

def count_income(budgets):
	income = 0
	for budget_item in budgets:
		
		if (budget_item.type.debit_or_credit.type == 'Credit'):
			income += budget_item.amount
			
		#else:
		#	total += budget_item.amount

	return income

def count_total(budgets):
	total = 0
	
	for budget_item in budgets:
		
		if (budget_item.type.debit_or_credit.type == 'Debit'):
			total += budget_item.amount
			
		#else:
		#	total += budget_item.amount

	return total
			
def get_budget(request):

	if request.method == "GET": 
		locale.setlocale( locale.LC_ALL, '' )
		print(locale.getlocale)
		if 'User' in request.session:
			user = User.objects.get(pk = request.session['User'])
			mode = "all"
			start_date = datetime.datetime.strptime(str(date.today()),"%Y-%m-%d") + timedelta(days = -7)
			budgets_all = Budget.objects.filter(user_id = user.id).filter(date__range = [start_date, date.today()]).order_by('date')
			paginator = Paginator(budgets_all, 6)

			page = request.GET.get('page')
			num = []

			try:
				budgets = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				budgets = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				budgets = paginator.page(paginator.num_pages)

			for y in range(2016, datetime.datetime.now().year+1):
				num.append(y)

			total_spending = count_total(budgets_all)
			income = count_income(budgets_all)
			number_of_pages = range(0, paginator.num_pages)
			return render(request, template_name="task_scheduler/budget.html", context={'budgets': budgets,
																						'num': num,
																						'total': total_spending,
																					    'income': income,
																					    'mode': mode,
																					    'number_of_pages': number_of_pages, })
		else:
			return redirect('/scheduler/login')

	elif request.method == "POST":
		if 'User' in request.session:
			user = User.objects.get(pk = request.session['User'])
			num = []
			for y in range(2016, datetime.datetime.now().year+1):
				num.append(y)
			
			mode = request.POST.get("selectpicker")
			
			if mode == "all":
				budgets = Budget.objects.filter(user_id = user.id).order_by('date')
				
			elif mode == "datepicker":
				search_date = request.POST.get("datepicker")
				budgets = Budget.objects.filter(user_id = user.id).filter(date = search_date).order_by('date')
				
			elif mode == "weekpicker":
				start_date = request.POST.get("datepicker")
				end_date = datetime.datetime.strptime(start_date,"%Y-%m-%d") + timedelta(days = 7)
				budgets = Budget.objects.filter(user_id = user.id).filter(date__range = [start_date, end_date]).order_by('date')

			elif mode == "monthpicker":
				month_year = request.POST.get("datepicker")
				month = month_year[0:2]
				year = month_year[3:7]
				start_dates = ["01", "08", "15", "22", "29"]
				week_spendings = []
				week_incomes = []

				for start_date in start_dates:
					start_week = datetime.datetime.strptime(str(year) + '-' + str(month) + '-' + str(start_date), "%Y-%m-%d")
					end_week = start_week + timedelta(days = 7)
					budgets = Budget.objects.filter(user_id = user.id).filter(date__range = [start_week, end_week]).order_by('date')
					week_spending = count_total(budgets)
					week_income = count_income(budgets)

					week_spendings.append(week_spending)
					week_incomes.append(week_income)

				
				total_spending = 0
				total_income = 0

				for spending in week_spendings:
					total_spending += spending
				for income in week_incomes:
					total_income += income

				return render(request, template_name="task_scheduler/budget.html", context={'budgets': budgets,
																						'num': num,
																						'total': total_spending,
																						'income': total_income,
																						'week_spendings': week_spendings,
																					    'week_incomes': week_incomes,
																					    'mode': mode, })
			elif mode == "yearpicker":
				month_spendings = []
				month_incomes = []
				
				for i in range(1, 13):
					budgets = Budget.objects.filter(user_id = user.id).filter(date__year = request.POST.get("yearpicker")).filter(date__month = i).order_by('date')
					month_spending = count_total(budgets)
					month_income = count_income(budgets)

					month_spendings.append(month_spending)
					month_incomes.append(month_income)

				total_spending = 0
				total_income = 0

				for spending in month_spendings:
					total_spending += spending
				for income in month_incomes:
					total_income += income

				paginator = Paginator(budgets, 6)
				page = request.GET.get('page')

				try:
					budgets = paginator.page(page)
				except PageNotAnInteger:
				# If page is not an integer, deliver first page.
					budgets = paginator.page(1)
				except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
					budgets = paginator.page(paginator.num_pages)

				return render(request, template_name="task_scheduler/budget.html", context={'budgets': budgets,
																						'num': num,
																						'total': total_spending,
																						'income': total_income,
																						'month_spendings': month_spendings,
																					    'month_incomes': month_incomes,
																					    'mode': mode, })

			else:
				budgets = Budget.objects.filter(user_id = user.id)
			
			total_spending = count_total(budgets)
			income = count_income(budgets)

			paginator = Paginator(budgets, 6)
			page = request.GET.get('page')

			try:
				budgets = paginator.page(page)
			except PageNotAnInteger:
			# If page is not an integer, deliver first page.
				budgets = paginator.page(1)
			except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
				budgets = paginator.page(paginator.num_pages)

			number_of_pages = range(0, paginator.num_pages)

			return render(request, template_name="task_scheduler/budget.html", context={'budgets': budgets,
																						'num': num,
																						'total': total_spending,
																					    'income': income,
																					    'mode': mode,
																					    'number_of_pages': number_of_pages, })
		else:
			return redirect('/scheduler/login')

def edit_budget(request, budget_pk, page_number):
	if request.method == 'GET':
		if 'User' in request.session:
			user = User.objects.get(pk = request.session['User'])
			budget = Budget.objects.get(pk = budget_pk)
			budget_date = datetime.datetime.strftime(budget.date, '%Y-%m-%d')
			budget_type = BudgetType.objects.filter(user_id = user.id)
			return render(request, template_name="task_scheduler/editbudget.html", context={'budget': budget,
																							 'budget_type': budget_type,
																							 'budget_date': budget_date,})
		else:
			return redirect("/scheduler/login")
	else:
		if 'User' in request.session:
			maketrans = str.maketrans
			budget = Budget.objects.get(pk = budget_pk)

			budget.name = request.POST.get("id_name")
			budget.date = datetime.datetime.strptime(request.POST.get("id_date"),"%Y-%m-%d")
			amount = request.POST.get("id_amount")
			amount = amount.translate(maketrans(',.', '.,'))
			budget.amount = amount.replace(",", "")
			type_id = request.POST.get("id_type")
			budget_type = BudgetType.objects.get(pk = type_id)
			budget.type = budget_type

			budget.save()
			return redirect("/scheduler/budget?page=" + page_number)
		else:
			return redirect("/scheduler/login")

def add_budget(request):
	if 'User' in request.session:
		user = User.objects.get(pk = request.session['User'])
		types = BudgetType.objects.filter(user_id = user.id)
		if (request.method == "POST"):
			form = BudgetForm(request.POST)
			if (form.is_valid):
				post = form.save(commit = False)
				type_id = request.POST.get("type")
				if (type_id != "none"):
					post.type = BudgetType.objects.get(pk = type_id)
				else:
					budget_type_name = request.POST.get("type_name")
					creditordebit = request.POST.get("type_creditordebit")
					budget_type_creditordebit = DebitOrCredit.objects.get(pk = creditordebit)
					
					budget_type = BudgetType.objects.create_budget_type(budget_type_name, budget_type_creditordebit, user)
					budget_type.save()
					post.type = budget_type
				post.user_id = user.id
				post.save()
			return redirect("/scheduler/budget")
		else:
			form = BudgetForm()
			return render(request, template_name="task_scheduler/newspending.html", context={'form': form,
																							 'types': types,})
	else:
		return redirect('/scheduler/login')

def delete_budget(request, budget_pk, page_number):
	if 'User' in request.session:
		user = User.objects.get(pk = request.session['User'])
		budget = Budget.objects.get(pk = budget_pk)
		budget.delete()
		return redirect("/scheduler/budget?page=" + page_number)
	else:
		return redirect("/scheduler/login")
	