from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import *


from django.contrib.auth import views as auth_views

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
url (r'^$', auth_views.LoginView.as_view(template_name='people/login.html'), name='login'),
url(r'^export/csv/$', export_registros_csv, name='export_registros_csv_list'),
url(r'^genera/clave/$', genera_clave, name='genera_clave'),
url(r'^generallaves/publica_privada/$', genera_llaves_publica_privada, name='genera_llaves_publica_privada'),
url(r'^descarga/llave_publica/$', descargar_llave_publica, name='descargar_llave_publica'),
url(r'^descarga/llave_privada/$', descargar_llave_privada, name='descargar_llave_privada'),
url(r'^firmardocumento/$', FirmarDocumento.as_view(), name='firmar_documento'),
url(r'^validarfirma/$', ValidarFirma.as_view(), name='valida_firma'),
url(r'^people/(?P<id>\d+)/$', getColaboradorDetail, name='people_detail_colaborador'),
url(r'^usuario/create/$', ColaboradorCreate.as_view(), name='people_colaborador_create'),
url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='people/login.html'), name='login'),
url(r'^logout/$', auth_views.LogoutView.as_view(template_name='people/logout.html'), name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)