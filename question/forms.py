from django import forms
from .models import Aes
from people.models import Colaborador
from django.core.exceptions import ValidationError

class AesForm(forms.ModelForm):
	class Meta:
		model = Aes
		fields = '__all__'

		

	
