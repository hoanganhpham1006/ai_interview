from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.core.validators import FileExtensionValidator

class RegisterForm(UserCreationForm):
	class Meta():
		model = User
		fields = ["username", "password1", "password2"]
			
class UploadCvForm(forms.Form):
	title = forms.CharField(max_length=50)
	# file = forms.FileField(validators=FileExtensionValidator(allowed_extensions=['pdf']))
	file = forms.FileField()
