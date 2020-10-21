from django import forms
from .models import Colaborador
from django.core.exceptions import ValidationError


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class ColaboradorForm(forms.ModelForm):
	class Meta:
		model = Colaborador
		fields = ['foto',]#'__all__'
		#exclude = ('es_estudiante', 'es_docente','user')

class UserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email','username','password1','password2']

	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user

class EditProfileForm(UserChangeForm):

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email','password']
        