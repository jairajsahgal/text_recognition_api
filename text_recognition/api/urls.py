from django.urls import path, include
from .views import register, uploadImage,login_account
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/',register,name="register"),
    path('upload_image/',uploadImage,name="upload-image"),
    path('login/',login_account,name="login-account")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)