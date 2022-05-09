from django.shortcuts import render
# from .models import Faq, PersonalFaq, PersonalComment

# # Create your views here.

# def faq(request):
#     faqs = Faq.objects.all()
#     # inquiries = Faq.inquiries
#     # content = Faq.content
#     # created_at = Faq.created_at
#     # writer = Faq.writer
#     return render(request, 'faq.html', {'faqs' : faqs}) #inquiries, 'content' : content, 'create_at' : created_at, 'writer' : writer})


# def personalfaq(request):
#     faqs = Faq.objects.all()
#     inquiries = Faq.inquiries
#     content = Faq.content
#     created_at = Faq.created_at
#     writer = Faq.writer
#     return render(request, 'faq.html', {'inquiries' : inquiries, 'content' : content, 'create_at' : created_at, 'writer' : writer})