from email.mime import image
from hashlib import blake2b
from operator import mod
from django.db import models
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from django.contrib.auth import get_user_model
from django.forms import RegexField  # 장고(인증시스템)에서 사용하고 있는 유저모델

# Create your models here.
User = get_user_model()


# 내 실습 코드


# class Category(models.Model):
#     name = models.CharField(max_length=50, help_text="글 분류")
    
#     def __str__(self):
#         return self.name

# class Faq(models.Model):
#     INQUIRIES_CHOICES = [
#         ('일반', 'normal'),
#         ('계정', 'id'),
#         ('기타', 'ect'),
#     ]
#     inquiries = models.CharField(max_length=3, choices=INQUIRIES_CHOICES, default='일반')
#     content = models.TextField(verbose_name='내용')
#     created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True) # auto_now_add=True : 게시글 작성시 자동 날짜 입력
#     modified_on = models.DateTimeField(auto_now=True)
#     writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
#     modifier = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="Faq.writer+")
#     comment = models.TextField(verbose_name='답변', default='')

# class PersonalFaq(models.Model):
#     category = models.ManyToManyField(Category, help_text='선택해주세요.')
#     head = models.TextField(verbose_name='제목', default='')
#     content = models.TextField(verbose_name='내용')
#     email = models.CharField(max_length=3, verbose_name='이메일', default=None)
#     phone_number = models.CharField(max_length=3, verbose_name='전화번호', default=None)
#     image = models.ImageField(verbose_name='이미지', null=True, blank=True) # verbose_name : 관리자나 폼 등 일반 사용자쪽 페이지에 노출될 필드에 대한 이름 지정
#     created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True) # auto_now_add=True : 게시글 작성시 자동 날짜 입력
#     writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

# class PersonalComment(models.Model):
#     content = models.TextField(verbose_name='내용')
#     created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
#     modified_on = models.DateTimeField(auto_now=True)
#     post = models.ForeignKey(to='PersonalFaq', on_delete=models.CASCADE)   # 게시글 foreignKey 연결. 게시글이 삭제되면 댓글도 삭제되게 on_delete에 CASCADE 설정
#     writer = models.ForeignKey(to=User, on_delete=models.CASCADE) # 사용자 연결. 장고에서 만든 사용자 모델 연결
#     modifier = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="PersonalComment.writer+", null=True, blank=True)
#     reference = models.ManyToManyField(to='PersonalFaq', related_name="PersonalFaq.head+", blank=True)



# 강사 코드

class Faq(models.Model):
    CATEGORY_CHOICES = [
        ('1', '일반'),  # 1은 개발단에서 사용할 변수. 데이터베이스에 들어갈 값이 1, 2, 3이 될 것. 사용자가 볼 값이 일반, 계정 기타
        ('2', '계정'),  # 컴퓨터는 한글보다 숫자, 숫자보다 이진수를 처리하는게 빠름. 그래서 db에 일반보다는 1로 저장하는게 성능이 뛰어나질 수 있음
        ('3', '기타'),  # 데이터가 수억개 막 이렇게 들어가면, 이거 하나의 차이로 엄청난 성능 차이가 난대. 또한, 다국어 번역할때 1, 2, 3으로 언어에 맞게 번역시키면 용이할 거래
        # 근데 또, 1이 뭐고 4가 뭔지 모를때가 있을 수 있는데, 그럴 때는 django 공식문서 사례처럼 'FR'이렇게 쓰는게 더 좋대.
        # 그래서
        # CATEGORY_ONE = '1'
        # 을 지정하고 이걸 저 1에 넣는게. 무조건 변수상수로 만들어서 쓰는게 좋대. 뭐 한두번 쓸 내용이면 안그래도 되는데, 계속 쓸 내용이면 변수만들어서
        #  이게 권장사례래
        # shell에서 사용할 때는
        # faq = Faq(), faq.category = Faq.CATEGORY_ONE. faq.save() 이렇게 
    ]

    # Field 타입은 한번 지정하면 안바꾸는게 좋음. 데이터가 들어가있는 상태에선 수정이 어렵고, 위험성 있음. 경험했지
    # 강사는 소수점 아래 다 날려버린적 있대. 복구 하긴 했지만
    title = models.CharField(verbose_name='질문 제목', max_length=80)   # text field로 해도 되지만, character field가 더 적합함. 제목은 요약해서 적은 글씨로 쓰니까
    content = models.TextField(verbose_name='질문 내용')
    category = models.CharField(verbose_name='카테고리', max_length=2, choices=CATEGORY_CHOICES)

    created_at = models.DateTimeField(verbose_name='생성 일시', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='최종 수정 일시', auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='faq_created_by')    # 모델간의 연결을 위해 ForeignKey로 연결.
                                                                                                        # to=로 어떤 모델과 연결할지 지정(User)
                                                                                                        # orm은 역방향/정방향 참조가 있음
                                                                                                        # related_name은 실무에서 무조건 작성한대. 코드는 일관성있게 한가지 규칙으로
                                                                                                        # 작성해야 돼서
                                                                                                        # 어쨌든, related_name은, User 모델에서도 Faq 클래스를 한번에 불러올 상황이
                                                                                                        # 있음(이게 역방향 참조). 이때, 어떤 이름컬럼으로 호출하는데,
                                                                                                        # 이떄 콜하는 이름이 related_name.
                                                                                                        # 예를 들어, 해당 User의 모든 created_by를 불러올 때는 faq_created_by를
                                                                                                        # 호출할 것임.
                                                                                                        # 그래서 foreignKey가 하나일 때는, django에서 기본값으로 relate_name을
                                                                                                        # 아마 클래스명_set() 등으로 지정해서 넣을텐데, 이 foreignKey가 여러개이면
                                                                                                        # default값을 생성 못하니까 우리가 꼭 지정해줘야 함
    updated_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='faq_updated_by')

class Inquiry(models.Model):
    CATEGORY_CHOICES = [
    ('1', '일반'),  
    ('2', '계정'),  
    ('3', '기타'), 

    ]
    category = models.CharField(verbose_name='카테고리', max_length=2, choices=CATEGORY_CHOICES)
    title = models.CharField(verbose_name='질문 제목', max_length=80)
    email = models.EmailField(verbose_name='이메일', blank=True)    # Emailfield 자체에서 validators 사용중. 실제는 Charfield임
    phone = models.CharField(verbose_name='문자메시지', max_length=11, blank=True)
    is_email = models.BooleanField(verbose_name='이메일 수신 여부', max_length=11, default=False)   # 얘도 Charfield로 가능하긴 하대. 만약 체크/해제가 아닌 3개 이상의 선택이면
    is_phone = models.BooleanField(verbose_name='문자메시지 수신 여부', default=False)  # Charfield가 더 적합하대
    content = models.TextField(verbose_name='문의 내용')
    image = models.ImageField(verbose_name='이미지', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='생성 일시', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='최종 수정 일시', auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='inquiry_created_by')
    updated_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='inquiry_updated_by')

class Answer(models.Model): # 1대1 문의에 대한 답변
    content = models.TextField(verbose_name='답변내용')
    created_at = models.DateTimeField(verbose_name='생성 일시', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='최종 수정 일시', auto_now=True)

    inquiry = models.ForeignKey(to='Inquiry', on_delete=models.CASCADE)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='answer_created_by')
    updated_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='answer_updated_by')