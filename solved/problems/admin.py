from django.contrib import admin
from .models import Problem

class ProblemAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"
    
admin.site.register(Problem, ProblemAdmin)