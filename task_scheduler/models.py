from django.db import models

# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=20, unique=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(unique = True)
	password = models.CharField(max_length=200)
	monthly_budget_target = models.DecimalField(decimal_places=2, max_digits=99)
	total_saving = models.DecimalField(decimal_places=2, max_digits=99)

	def __str__(self):
		return self.first_name

class DebitOrCredit(models.Model):
	type = models.CharField(max_length=10)

	def __str__(self):
		return self.type

class Task(models.Model):
	task_name = models.CharField(max_length=50)
	start_date = models.DateField()
	end_date = models.DateField()
	description = models.TextField()
	user = models.ForeignKey("User", on_delete=models.CASCADE)

	def __str__(self):
		return self.task_name

class Currency(models.Model):
	currency_name = models.CharField(max_length=50)
	class Meta:
		verbose_name_plural = "Currencies"

	def __str__(self):
		return self.currency_name

class BudgetTypeManager(models.Manager):
    def create_budget_type(self, type_name, debit_or_credit, user):
        budget_type = self.create(type_name = type_name, debit_or_credit = debit_or_credit, user = user)
        
        return budget_type

class BudgetType(models.Model):
	type_name = models.CharField(max_length=50)
	debit_or_credit = models.ForeignKey("DebitOrCredit", on_delete=models.CASCADE)
	user = models.ForeignKey("User", on_delete=models.CASCADE)
	objects = BudgetTypeManager()

	def __str__(self):
		return self.type_name


class Budget(models.Model):
	name = models.CharField(max_length=50)
	date = models.DateField()
	amount = models.DecimalField(decimal_places=2, max_digits=99)
	user = models.ForeignKey("User", on_delete=models.CASCADE)
	type = models.ForeignKey("BudgetType", on_delete=models.CASCADE,)
	#currency = models.ForeignKey("Currency", on_delete=models.CASCADE)

	def __str__(self):
		return self.name
	