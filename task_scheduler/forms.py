from django import forms
from .models import Budget, User
import bcrypt

class BudgetForm(forms.ModelForm):
	class Meta:
		model = Budget
		fields = ('name', 'date', 'amount',)
		
class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password', 'monthly_budget_target', 'total_saving',)
		widgets = {
			'password': forms.PasswordInput(),
		}
	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		encrypted_password = bcrypt.hashpw(self.cleaned_data.get("password").encode('utf-8'), bcrypt.gensalt())
		user.password = encrypted_password
		if commit:
			user.save()
		return user


