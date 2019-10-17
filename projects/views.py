from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import RegisterForm, UploadCvForm

# Create your views here.
def home(response):
	return render(response, "base.html")

def upload(response):
	
	if response.method == 'POST' and response.FILES['document']:
		upload_file = response.FILES['document']

		file_save = FileSystemStorage()
		filename = file_save.save(upload_file.name, upload_file)
		file_url = file_save.url(filename)

		return render(response, "home/upload.html", {"file_url":file_url})
	return render(response, "home/upload.html")

def register(response):
	if response.method == "POST":
		form = RegisterForm(response.POST)
		if form.is_valid():
			un = form.cleaned_data.get('username')
			pss = form.cleaned_data.get('password1')
			print(un, pss)
			# form.save()
			return redirect("/login")
		else:
			print("invalid form")
			form = RegisterForm()
	else:
		form = RegisterForm()
	
	return render(response, "register/register.html", {"form":form})