from django.contrib.auth import get_user_model
from django.contrib import admin
from .models import Faq, Inquiry, Answer, User

# # Register your models here.


# class UserAdmin(admin.ModelAdmin):
#     search_fields = ('user__username', 'user__email', 'user__phone')
User = get_user_model()

class CommentInline(admin.TabularInline):
    model = Answer
    extra = 1
    min_num = 0
    max_num = 10
    verbose_name = "답변"
    verbose_name_plural = "답변"



@admin.register(Faq)
class FaqModelAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "updated_at")
    list_filter = ('category', )
    search_fields = ('title', )
    search_help_text = '제목 입력'
    readonly_fields = ('updated_at', )


@admin.register(Inquiry)
class InquiryqModelAdmin(admin.ModelAdmin):
    list_display = ( "category", "status", "title", "created_at", "created_by")
    list_filter = ('category', "status")
    search_fields = ['user__username', 'user__email', 'phone']
    search_help_text = 'username, phone, email'
    readonly_fields = ("created_at", )
    inlines = [CommentInline]

    actions = ['make_calling']    # admin에 선택한 게시글 모두 지우기 같은 특수기능 추가. 이런 기능은 함수 직접 만들어서 넣어주면 됨

    def make_calling(modeladmin, request, queryset):      # queryset은 페이지에서 전송한 데이터가 들어옴. 데이터 세개 선택/전송했으면 세개를 한셋으로
        for item in queryset:
            if item.is_email == True:
                print(str(item.id) + "번째 글 메일 발송")
            if item.is_phone == True:
                print(str(item.id) + "번째 글 문자 발송")