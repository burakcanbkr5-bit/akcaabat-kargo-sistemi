import random
import string
from django.db import models
from django.utils import timezone  # Bunu ekledik

def takip_no_olustur():
    """Örn: AKC-847291 gibi benzersiz bir numara üretir."""
    prefix = "AKC-"
    sayilar = ''.join(random.choices(string.digits, k=6))
    return prefix + sayilar

class Kurye(models.Model):
    isim = models.CharField(max_length=100, verbose_name="Kurye Adı")
    bolge = models.CharField(max_length=100, verbose_name="Dağıtım Bölgesi")
    durum_secenekleri = [('Cevrimici', 'Çevrimiçi'), ('Yolda', 'Yolda')]
    durum = models.CharField(max_length=20, choices=durum_secenekleri, default='Cevrimici', verbose_name="Çalışma Durumu")
    puan = models.FloatField(default=5.0, verbose_name="Hizmet Puanı")
    foto_url = models.URLField(blank=True, default="https://randomuser.me/api/portraits/men/1.jpg", verbose_name="Fotoğraf URL")

    class Meta:
        verbose_name = "Kurye"
        verbose_name_plural = "Kuryeler"

    def __str__(self):
        return self.isim

class Kargo(models.Model):
    DURUM_SECENEKLERI = [
        ('Hazırlanıyor', 'Hazırlanıyor'),
        ('Yolda', 'Yolda'),
        ('Şubede', 'Şubede'),
        ('Teslim Edildi', 'Teslim Edildi'),
    ]

    takip_no = models.CharField(
        max_length=12, 
        unique=True, 
        default=takip_no_olustur, 
        editable=False, 
        verbose_name="Takip Numarası"
    )
    
    alici_ad = models.CharField(max_length=100, verbose_name="Alıcı Adı Soyadı")
    kargo_icerigi = models.TextField(verbose_name="Kargo İçeriği")
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='Hazırlanıyor', verbose_name="Kargo Durumu")
    kurye = models.ForeignKey(Kurye, on_delete=models.SET_NULL, null=True, blank=True, related_name="kargolar", verbose_name="Sorumlu Kurye")
    kayit_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    class Meta:
        verbose_name = "Kargo"
        verbose_name_plural = "Kargolar"

    def __str__(self):
        return f"{self.takip_no} - {self.alici_ad}"


    def ai_tahmin_suresi(self):
        """Kargonun durumuna göre dinamik süre tahmini yapar"""
        if self.durum == 'Teslim Edildi':
            return "Teslimat Tamamlandı"
        
       
        gecen_sure = timezone.now() - self.kayit_tarihi
        saat_farki = gecen_sure.total_seconds() / 3600
        
         
        
        tahmin = max(0.5, 3.5 - saat_farki) 
        return f"{round(tahmin, 1)} Saat"