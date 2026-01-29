from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from takip import views

urlpatterns = [
    # Admin Paneli
    path('admin/', admin.site.urls),

    # Genel Sayfalar
    path('', views.ana_sayfa, name='ana_sayfa'),
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('kargo-takip/', views.kargo_takip, name='kargo_takip'),

    # Kargo Yönetimi (Detay, Ekle, Güncelle, Sil)
    path('kargo/<int:pk>/', views.kargo_detay, name='kargo_detay'),
    path('yeni-kargo/', views.kargo_ekle, name='kargo_ekle'),
    path('kargo/guncelle/<int:pk>/', views.kargo_guncelle, name='kargo_guncelle'),
    path('kargo/sil/<int:pk>/', views.kargo_sil, name='kargo_sil'),

    # Kurye ve Kimlik Doğrulama (Login, Logout, Register)
    path('kuryeler/', views.kurye_listesi, name='kurye_listesi'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.kayit_ol, name='register'), # Kayıt olma yolu eklendi
]

# Medya ve Statik dosyaları geliştirme ortamında (DEBUG=True) sunmak için:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)