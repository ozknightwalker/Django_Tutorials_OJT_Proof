from django.contrib import admin
from .models import *
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['text']}),
        ('Date information', {'fields': ['published'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('text', 'published', 'published_recently')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)