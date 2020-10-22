from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import View
from .models import Colaborador
from .forms import ColaboradorForm,UserForm,EditProfileForm, FirmaForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.http import HttpResponse
import csv

import mimetypes
import os.path
from django.core.files.storage import default_storage

from django.contrib.auth.decorators import login_required
import mimetypes
#usado para encriptación AES
from cryptography.fernet import Fernet

#usado para encriptacion asimetrica
import Crypto
from Crypto.PublicKey import RSA
import binascii
from Crypto.Hash import MD5#, SHA256
from Crypto.Signature import PKCS1_v1_5

#messages
from django.contrib import messages

private_keyy = None
public_keyy = None
signature = None

@login_required
def genera_clave(request): #genera clave Encriptacion AES (Encriptación simetrico)
	clave = Fernet.generate_key()
	response = HttpResponse(clave, content_type='text/liquid')
	response['Content-Disposition'] = 'attachment; filename="clave.key"'
	return response

@login_required
def genera_llaves_publica_privada(request): #encriptacion asimetrica
	global private_keyy
	global public_keyy

	random_generator = Crypto.Random.new().read
	private_keyy = RSA.generate(1024, random_generator)
	public_keyy = private_keyy.publickey()
	messages.success(request, 'LLaves publica y privada generadas con éxito')
	return redirect('question_recents_list')

@login_required
def descargar_llave_publica(request):
	if public_keyy is not None:
		public_key_ascci = public_keyy.exportKey(format='DER')
		public_key_ascci = binascii.hexlify(public_key_ascci).decode('utf8')

		response = HttpResponse(public_key_ascci, content_type='text/plain')
		response['Content-Disposition'] = 'attachment; filename="clave_publica.txt"'
		return response
	else:
		messages.error(request, 'Por favor primero genere las llaves publica y privada en el menú')
		return redirect('question_recents_list')

@login_required	
def descargar_llave_privada(request):
	if private_keyy is not None:
		private_key_ascci = private_keyy.exportKey(format='DER')
		private_key_ascci = binascii.hexlify(private_key_ascci).decode('utf8')

		response = HttpResponse(private_key_ascci, content_type='text/plain')
		response['Content-Disposition'] = 'attachment; filename="clave_privada.txt"'
		return response
	else:
		messages.error(request, 'Por favor primero genere las llaves publica y privada en el menú')
		return redirect('question_recents_list')

class FirmarDocumento(LoginRequiredMixin, View):
	def get(self, request):
		preForm = FirmaForm()
		mensaje = "Firmar"
		return render(request,'people/firma_form.html', {'form': preForm, 'mensaje': mensaje})

		
	def post(self, request):
		global signature
		bound_form = FirmaForm(request.POST, request.FILES)

		if bound_form.is_valid():
			if private_keyy is not None:
				new_object = bound_form.save(commit=False)
				new_object.save()
				#print(new_object.key)

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
				#priv_key = RSA.importKey(private_keyy)

				signer = PKCS1_v1_5.new(private_keyy)
				md5_object = MD5.new()
				print("valor de md5 ", md5_object)
				print("signer ", signer)
				md5_object.update(data.encode())
				signature = signer.sign(md5_object)
				#print("La firma es ", signature)

				messages.success(request, f'Archivo firmado con éxito, la firma es: {signature}')
				return redirect('question_recents_list')
				# encrypted_data = f.encrypt(data.encode())
				# response = HttpResponse(encrypted_data, content_type='text/plain')
				# response['Content-Disposition'] = 'attachment; filename="archivoencriptado.txt"'
				# return response
				#return render(request, 'question/index.html')
			else:
				messages.error(request, f'Por favor primero genere las llaves publica y privada en el menú, y luego puede firmar el documento')
				return redirect('question_recents_list')
		else:
			return render(request,'people/firma_form.html',{'form': bound_form,})

class ValidarFirma(LoginRequiredMixin, View):
	def get(self, request):
		preForm = FirmaForm()
		mensaje = ""
		return render(request,'people/firma_form.html', {'form': preForm, 'mensaje': mensaje})

		
	def post(self, request):
		bound_form = FirmaForm(request.POST, request.FILES)

		if bound_form.is_valid():
			if private_keyy is not None:
				new_object = bound_form.save(commit=False)
				new_object.save()
				#print(new_object.key)

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
				#priv_key = RSA.importKey(private_keyy)

				signer = PKCS1_v1_5.new(public_keyy)
				md5_object = MD5.new()
				print("valor de md5 ", md5_object)
				print("signer ", signer)
				md5_object.update(data.encode())
				result = signer.verify(md5_object, signature)
				#print("La firma es ", signature)
				if result:
					messages.success(request, f'¡¡ FIRMA AUTENTICADA CON ÉXITO !!')
				else:
					messages.warning(request, f'La firma no se pudo autenticar')

				return redirect('question_recents_list')
				# encrypted_data = f.encrypt(data.encode())
				# response = HttpResponse(encrypted_data, content_type='text/plain')
				# response['Content-Disposition'] = 'attachment; filename="archivoencriptado.txt"'
				# return response
				#return render(request, 'question/index.html')
			else:
				messages.error(request, f'Por favor primero genere las llaves publica y privada en el menú, y luego puede firmar el documento y validar la firma')
				return redirect('question_recents_list')
		else:
			return render(request,'people/firma_form.html',{'form': bound_form,})
		

@login_required
def export_registros_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrousuarios.csv"'

    writer = csv.writer(response)
    writer.writerow(['username', 'email', 'Nombres','Apellidos' ,'Contraseña' ])
    users = User.objects.values('username','email','first_name','last_name','password').values_list('username','email','first_name','last_name','password')
    
    for user in users:
	    writer.writerow(user)

    return response 

@login_required
def getColaboradorDetail(request, id):
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')

	colabDetail = get_object_or_404(Colaborador, pk=id)
	return render(request,'people/people_detail_colaborador.html', {'colaborador': colabDetail, 'colaboradores_top': colab , 'tag_list': tags})


class ColaboradorCreate(View):

	def get(self, request):
		user_form = UserForm()

		return render(request,'people/colaborador_form.html', {'form': ColaboradorForm,'user_form': user_form })

	def post(self, request):
				
		user_form = UserForm(request.POST)
		bound_form = ColaboradorForm(request.POST, request.FILES)

		if bound_form.is_valid() and user_form.is_valid():
			userName = user_form.cleaned_data['username']
			eMail = user_form.cleaned_data['email']
			passWord = user_form.cleaned_data['password1']

			if not (User.objects.filter(username=userName).exists() or User.objects.filter(email=eMail).exists()):
				foto = bound_form.cleaned_data['foto']				
				created_user = user_form.save()
				#bound_form = ColaboradorForm(request.POST, request.FILES)
				new_object = Colaborador.objects.get(user=created_user )
				new_object.foto = foto
				new_object.save()
				return render(request, 'people/people_detail_colaborador.html', {'colaborador': new_object,})
			else:
				raise forms.ValidationError('El usuario o Email ya existe')
			


			
		else:
			return render(request,'people/colaborador_form.html',{'form': bound_form, 'user_form': user_form, })

def profile(request):
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	
	colaborator = Colaborador.objects.get(user=request.user)

	args= {'user': request.user,'colaborator': colaborator,'colaboradores_top': colab , 'tag_list': tags, }
	return render(request, 'people/profile.html',args)

def edit_profile(request):
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	colaborator = Colaborador.objects.get(user=request.user)

	if request.method == 'POST':
		

		form = EditProfileForm(request.POST, instance=request.user)
		form_colab_porfoto = ColaboradorForm(request.POST, request.FILES, instance=request.user )

		if form.is_valid() and form_colab_porfoto.is_valid():
			newFoto = form_colab_porfoto.cleaned_data['foto']
			form.save()
			#form_colab_porfoto.save(commit=False)
			#form_colab_porfoto.foto = newFoto
			#form_colab_porfoto.save()
			if newFoto is not None: #it is not working mmmmmm...
				colaborator.foto = newFoto
				colaborator.save()
			args= {'user': request.user, 'colaborator': colaborator, 'colaboradores_top': colab , 'tag_list': tags, }
			return render(request, 'people/profile.html',args)
			#return redirect('/profile/')
	else:
		form = EditProfileForm(instance=request.user)
		form_colab_porfoto = ColaboradorForm(request.POST)
		args = {'form': form,'form_colab_porfoto': form_colab_porfoto ,'colaborator': colaborator,'colaboradores_top': colab , 'tag_list': tags, }
		return render(request, 'people/edit_profile.html', args)

def change_password(request):
	colaborator = Colaborador.objects.get(user=request.user)
	colab =  Respuesta.objects.values('Colaborador','Colaborador__user__first_name', 'Colaborador__user__last_name').annotate(Count('Colaborador')).order_by('-Colaborador__count')[:5]#Colaborador.objects.all()[:5]
	for i in range(len(colab)):
		colab[i]['Colaborador'] = Colaborador.objects.get(pk=colab[i]['Colaborador'])
	tags = Tag.objects.all().order_by('name')
	

	if request.method == 'POST':
		

		form = PasswordChangeForm(data=request.POST, user=request.user)

		if form.is_valid():
			form.save()
			args= {'user': request.user,'colaborator': colaborator ,'colaboradores_top': colab , 'tag_list': tags, }
			update_session_auth_hash(request, form.user)
			return render(request, 'people/profile.html',args)
			#return redirect('/profile/')
		else:
			args= {'form': form,'user': request.user,'colaborator': colaborator ,'colaboradores_top': colab , 'tag_list': tags, }
			return render(request, 'people/change_password.html',args)
	else:
		form = PasswordChangeForm(user=request.user)
		args = {'form': form,'colaborator': colaborator ,'colaboradores_top': colab , 'tag_list': tags, }
		return render(request, 'people/change_password.html', args)





