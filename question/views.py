from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from people.models import Colaborador
from .forms import AesForm

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

import mimetypes
import os.path
from cryptography.fernet import Fernet
from django.core.files.storage import default_storage
from django.contrib.auth.mixins import LoginRequiredMixin

#messages
from django.contrib import messages

@login_required
@never_cache
def index(request):
	return render(request,'question/index.html')



class RecentsQuestionList(LoginRequiredMixin, View): 
	def get(self, request):
		return render(request, 'question/index.html')


class AesEncriptar(LoginRequiredMixin, View):
	def get(self, request):
		preForm = AesForm()
		mensaje = "Encriptar"
		return render(request,'question/question_form.html', {'form': preForm, 'mensaje': mensaje})

		
	def post(self, request):
		bound_form = AesForm(request.POST, request.FILES)

		if bound_form.is_valid():
			new_object = bound_form.save(commit=False)
			new_object.save()
			#print(new_object.key)

			#import pdb; pdb.set_trace()
			# el archivo que contiene la clave
			my_file=request.FILES['key']
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			media_path = os.path.join(BASE_DIR,'media/archivos/')
			full_path=os.path.join(media_path,my_file.name)
			#print(full_path)

			f = default_storage.open(full_path, 'r')
			data = f.read()
			f.close()
			#print(data)
			try:
				f = Fernet(data)
			except:
				messages.warning(request, 'Hubo un error al encriptar, por favor verificar')
				return redirect('question_recents_list')
			
			# el archivo que se quiere encriptar
			my_file=request.FILES['fileupload']
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			media_path = os.path.join(BASE_DIR,'media/archivos/')
			full_path=os.path.join(media_path,my_file.name)
			#print(full_path)

			filedata = default_storage.open(full_path, 'r')
			data = filedata.read()
			filedata.close()
			#print(data)
			encrypted_data = f.encrypt(data.encode())
			response = HttpResponse(encrypted_data, content_type='text/plain')
			response['Content-Disposition'] = 'attachment; filename="archivoencriptado.txt"'
			return response
			#return render(request, 'question/index.html')
		else:
			return render(request,'question/question_form.html',{'form': bound_form,})


class AesDesencriptar(LoginRequiredMixin, View):
	def get(self, request):
		preForm = AesForm()
		return render(request,'question/question_form.html', {'form': preForm, })
		
	def post(self, request):
		bound_form = AesForm(request.POST, request.FILES)

		if bound_form.is_valid():
			new_object = bound_form.save(commit=False)
			new_object.save()
			#print(new_object.key)

			#import pdb; pdb.set_trace()
			# el archivo que contiene la clave
			my_file=request.FILES['key']
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			media_path = os.path.join(BASE_DIR,'media/archivos/')
			full_path=os.path.join(media_path,my_file.name)
			#print(full_path)

			f = default_storage.open(full_path, 'r')
			data = f.read()
			f.close()
			#print(data)
			try:
				f = Fernet(data)
			except:
				messages.warning(request, 'Hubo un error al desencriptar, por favor verificar')
				return redirect('question_recents_list')

			

			# el archivo que se quiere encriptar
			my_file=request.FILES['fileupload']
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			media_path = os.path.join(BASE_DIR,'media/archivos/')
			full_path=os.path.join(media_path,my_file.name)
			#print(full_path)

			filedata = default_storage.open(full_path, 'r')
			data = filedata.read()
			filedata.close()
			#print(data)
			try:
				decrypted_data = f.decrypt(data.encode())
			except Exception:
				error = 'Las firmas no coinciden '
				return render(request,'question/question_form.html',{'form': bound_form, 'error': error})

			response = HttpResponse(decrypted_data, content_type='text/plain')
			response['Content-Disposition'] = 'attachment; filename="archivo_desencriptado.txt"'
			return response
			#return render(request, 'question/index.html')
		else:
			return render(request,'question/question_form.html',{'form': bound_form,})
		



