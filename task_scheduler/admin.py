from django.contrib import admin
from .models import User, Task, Currency, Budget, BudgetType, DebitOrCredit
from .forms import UserForm
# Register your models here.

class UserFormAdmin(admin.ModelAdmin):
	form = UserForm

admin.site.register(User, UserFormAdmin)
admin.site.register(Task)
admin.site.register(Currency)
admin.site.register(Budget)
admin.site.register(BudgetType)
admin.site.register(DebitOrCredit)