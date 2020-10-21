from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import *


from django.contrib.auth import views as auth_views

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
#path(‘<str:filepath>/‘, views.download_file)
urlpatterns = [
url (r'^$', auth_views.LoginView.as_view(template_name='people/login.html'), name='login'),
url(r'^export/csv/$', export_registros_csv, name='export_registros_csv_list'),
url(r'^genera/clave/$', genera_clave, name='genera_clave'),
url(r'^people/(?P<id>\d+)/$', getColaboradorDetail, name='people_detail_colaborador'),
url(r'^usuario/create/$', ColaboradorCreate.as_view(), name='people_colaborador_create'),
url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='people/login.html'), name='login'),
url(r'^logout/$', auth_views.LogoutView.as_view(template_name='people/logout.html'), name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)