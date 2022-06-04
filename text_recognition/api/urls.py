from django.urls import path, include
from .views import register, uploadImage,login_account, displayImages, get_text_from_image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/',register,name="register"),
    path('upload_image/',uploadImage,name="upload-image"),
    path('login/',login_account,name="login-account"),
    path('picture-list/',displayImages,name="display-pictures"),
    path('picture-ocr/',get_text_from_image,name="picture-ocr"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)