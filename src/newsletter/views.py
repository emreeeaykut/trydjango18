from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import ContactForm, SignUpForm
from .models import SignUp
# Create your views here.

def home(request):
	title = "Sign Up Now"
	form = SignUpForm(request.POST or None)

	context = {
		"title": title,
		"form": form
	}

	if form.is_valid():
		# form.save()
		print request.POST['email']
		instance = form.save(commit=False)

		full_name = form.cleaned_data.get("full_name")
		if not full_name:
			full_name = "YOK"
		instance.full_name = full_name
		# if not instance.full_name:
		# 	instance.full_name = "emre"
		instance.save()
		context = {
			"title": "Thank you"
		}

	if request.user.is_authenticated() and request.user.is_staff:
		#print(SignUp.objects.all())
		# i = 1
		# for instance in SignUp.objects.all():
		# 	print(i)
		# 	print(instance.full_name)
		# 	i += 1

		#queryset = SignUp.objects.all().order_by('-timestamp').filter(full_name__iexact="emre")#icontains
		#queryset = SignUp.objects.all().order_by('-timestamp')
		# queryset = SignUp.objects.get(full_name="erme")
		queryset = SignUp.objects.order_by('email').first()

		context = {
			"queryset": queryset
		}
	
	return render(request, "home.html", context)

def contact(request):
	title = 'Contact Us'
	title_align_center = True
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key, value in form.cleaned_data.iteritems():
		# 	print key, value
		from_email = form.cleaned_data.get("email")
		from_message = form.cleaned_data.get("message")
		from_full_name = form.cleaned_data.get("full_name")
		# print email,message,full_name
		subject = 'iletisim form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'emreeeaykut@hotmail.com']
		contact_message = "%s: %s via %s"%(
			from_full_name, 
			from_message, 
			from_email)
		some_html_message = """
		<h1>Merhaba</h1>
		"""

		send_mail(subject,
			contact_message,
			from_email,
			to_email,
			html_message = some_html_message,
			fail_silently=True)

	context = {
		"form": form,
		"title": title,
		"title_align_center": title_align_center,
	}
	return render(request, "forms.html", context)







