from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Colaborador(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	foto = models.ImageField(upload_to='fotoscolaboradores',default = 'fotoscolaboradores/profile.png', null=True, blank=True)

	def __str__(self):
		return self.user.first_name.title()

	
	def get_absolute_url(self):
		return reverse('people_detail_colaborador', kwargs={'id': self.id})

	def fotoxs(self):
		if self.foto:
			return mark_safe('<img src="{0}" width="60" height="60" alt="Sin foto">'.format(self.foto.url))
		else:
			return mark_safe('<img src="profile.png" width="60" height="60" alt="Usuario sin foto"/>')

	def admin_foto(self):
		if self.foto:
			return mark_safe('<img src="{0}" width="100" height="110" alt="Sin foto">'.format(self.foto.url))
		else:
			return mark_safe('<img src="profile.png" width="120" height="100" alt="Usuario sin foto"/>')

	def create_profile(sender, **kwargs):
		user = kwargs["instance"]
		
		if kwargs["created"]:
			user_profile = Colaborador.objects.create(user=user)
			user_profile.save()
		
	post_save.connect(create_profile, sender=User)

