from django.contrib import admin
from .models import userd, FashionModel
# Register your models here.

admin.site.register(userd)

admin.site.register(FashionModel)

class TodoListAdmin(admin.ModelAdmin):
	list_display = ("title", "created", "due_date")

class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name",)
