from django.shortcuts import render, render_to_response, redirect
from task_scheduler.models import User
from task_scheduler.forms import UserForm
import bcrypt
import datetime

def register(request):
	if (request.method == "POST"):
		form = UserForm(request.POST)
		if (form.is_valid):
			user = form.save(commit=False)
			user.save()
		return redirect("/scheduler/index")
	else:
		form = UserForm
		return render(request, template_name="task_scheduler/register.html", context={'form': form})

def login(request):
	if (request.method == "POST"):
		username = request.POST.get("username")
		password = request.POST.get("password")
		
		user = User.objects.get(username = username)
		if (bcrypt.hashpw(password.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8')):
			request.session['User'] = user.id
			request.session['Username'] = user.username
			return redirect('/scheduler/index')
		else:
			return render(request, template_name="task_scheduler/login.html")
	else:
		return render(request, template_name="task_scheduler/login.html")

def logout(request):
	del request.session['User']
	return redirect('/scheduler/login')


