from django.conf.urls import url

from .views import *

urlpatterns = [
url(r'^bienvenido/$',index, name='question_recents_list'),
url(r'^encriptar/$',AesEncriptar.as_view(), name='aes_encriptar'),
url(r'^desencriptar/$',AesDesencriptar.as_view(), name='aes_desencriptar'),

]