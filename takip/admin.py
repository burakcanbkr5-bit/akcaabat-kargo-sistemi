from django.contrib import admin
from .models import Kargo, Kurye

# Kargo modelinin admin paneli görünümü
@admin.register(Kargo)
class KargoAdmin(admin.ModelAdmin):
    # Listeleme ekranında görünecek sütunlar
    list_display = ('takip_no', 'alici_ad', 'durum', 'kurye', 'kayit_tarihi')
    
    # Sağ taraftaki filtreleme seçenekleri
    list_filter = ('durum', 'kayit_tarihi', 'kurye')
    
    # Arama kutusu kriterleri
    search_fields = ('takip_no', 'alici_ad')
    
    # Otomatik oluşan takip numarasının değiştirilmesini engeller
    readonly_fields = ('takip_no',)
    
    # Sayfa başına gösterilecek kayıt sayısı
    list_per_page = 20

# Kurye modelinin admin paneli görünümü
@admin.register(Kurye)
class KuryeAdmin(admin.ModelAdmin):
    # Listeleme ekranında görünecek sütunlar
    list_display = ('isim', 'bolge', 'durum', 'puan')
    
    # Listeden (tıklamadan) değiştirilebilecek alanlar
    list_editable = ('durum',)
    
    # Kuryeleri puanına ve bölgesine göre filtreleme
    list_filter = ('bolge', 'durum')
    
    # İsim ve bölgeye göre arama
    search_fields = ('isim', 'bolge')

# Not: admin.site.register(Kargo) satırlarını sildik çünkü yukarıdaki @ dekoratörleri bu işlemi zaten yapıyor.