from django.db import models


class Aes(models.Model):
    fileupload = models.FileField('Cargar archivo con los datos',upload_to = 'archivos/')
    key = models.FileField('Cargar archivo .key', upload_to = 'archivos/')

    def __str__(self):
        return self.id
		






