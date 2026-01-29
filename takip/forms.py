from django import forms
from .models import Kargo

class KargoEkleForm(forms.ModelForm):
    class Meta:
        model = Kargo
        # takip_no otomatik oluşturulacağı için formdan çıkarıldı
        fields = ['alici_ad', 'kargo_icerigi', 'durum', 'kurye'] 
        
        # Form elemanlarına modern Bootstrap görünümü kazandıralım
        widgets = {
            'alici_ad': forms.TextInput(attrs={
                'class': 'form-control rounded-pill', 
                'placeholder': 'Alıcının Adı Soyadı'
            }),
            'kargo_icerigi': forms.Textarea(attrs={
                'class': 'form-control rounded-4', 
                'rows': 3, 
                'placeholder': 'Paket içeriği hakkında kısa bilgi...'
            }),
            'durum': forms.Select(attrs={
                'class': 'form-select rounded-pill'
            }),
            'kurye': forms.Select(attrs={
                'class': 'form-select rounded-pill'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(KargoEkleForm, self).__init__(*args, **kwargs)
        # Personel için seçim kutularına varsayılan boş seçenek ekleyelim
        self.fields['durum'].empty_label = "Durum Seçiniz"
        self.fields['kurye'].empty_label = "Kurye Atayınız"