# Generated by Django 3.1.2 on 2020-10-21 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileupload', models.FileField(upload_to='archivos/', verbose_name='Cargar archivo con los datos')),
                ('key', models.FileField(upload_to='archivos/', verbose_name='Cargar archivo .key')),
            ],
        ),
    ]
