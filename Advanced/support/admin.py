from csv import list_dialects
from django.contrib import admin
from .models import Faq, PersonalFaq, PersonalComment, Category

# # Register your models here.

# admin.site.register(Category)

class CommentInline(admin.TabularInline):
    model = PersonalComment
    extra = 1
    min_num = 0
    max_num = 10


@admin.register(Faq)
class FaqModelAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "created_at", "modified_on", "writer", "comment", "modifier")



@admin.register(PersonalFaq)
class PersonalFaqModelAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "created_at", "writer")
    inlines = [CommentInline]