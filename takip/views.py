from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Kargo, Kurye
from .forms import KargoEkleForm

# --- GENEL SAYFALAR ---

def ana_sayfa(request):
    sorgu = request.GET.get('sorgu', '').strip()
    kargolar = []
    
    # İstatistikler
    toplam = Kargo.objects.count()
    yolda = Kargo.objects.filter(durum='Yolda').count()
    teslim = Kargo.objects.filter(durum='Teslim Edildi').count()

    if request.user.is_authenticated:
        # PERSONEL GİRİŞİ: Tüm kargoları listele ve filtrele
        kargolar = Kargo.objects.all().order_by('-kayit_tarihi')
        if sorgu:
            kargolar = kargolar.filter(
                Q(takip_no__icontains=sorgu) | Q(alici_ad__icontains=sorgu)
            )
    else:
        # MÜŞTERİ MODU: Sadece tam eşleşen takip no
        if sorgu:
            kargolar = Kargo.objects.filter(takip_no=sorgu)

    context = {
        'kargolar': kargolar,
        'sorgu': sorgu,
        'toplam': toplam,
        'yolda': yolda,
        'teslim': teslim,
    }
    return render(request, 'ana_sayfa.html', context)

def hakkimizda(request):
    return render(request, 'hakkimizda.html')

def iletisim(request):
    return render(request, 'iletisim.html')

def kargo_takip(request):
    return render(request, 'kargo_takip.html')

# --- ÜYELİK İŞLEMLERİ ---

def kayit_ol(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Hoş geldin {user.username}! Hesabın başarıyla oluşturuldu.")
            return redirect('ana_sayfa')
        else:
            messages.error(request, "Kayıt sırasında bir hata oluştu. Lütfen bilgileri kontrol edin.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# --- DETAY VE KURYE ---

def kargo_detay(request, pk):
    kargo = get_object_or_404(Kargo, pk=pk)
    return render(request, 'kargo_detay.html', {'kargo': kargo})

@login_required
def kurye_listesi(request):
    kuryeler = Kurye.objects.all()
    return render(request, 'kurye_listesi.html', {'kuryeler': kuryeler})

# --- PERSONEL İŞLEMLERİ (Yönetim) ---

@login_required
def kargo_ekle(request):
    if request.method == "POST":
        form = KargoEkleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Yeni kargo kaydı başarıyla eklendi.")
            return redirect('ana_sayfa')
    else:
        form = KargoEkleForm()
    return render(request, 'kargo_ekle.html', {'form': form})

@login_required
def kargo_guncelle(request, pk):
    kargo = get_object_or_404(Kargo, pk=pk)
    if request.method == "POST":
        form = KargoEkleForm(request.POST, request.FILES, instance=kargo)
        if form.is_valid():
            form.save()
            messages.success(request, f"#{kargo.takip_no} numaralı kargo güncellendi.")
            return redirect('ana_sayfa')
    else:
        form = KargoEkleForm(instance=kargo)
    return render(request, 'kargo_ekle.html', {'form': form, 'guncelle': True})

@login_required
def kargo_sil(request, pk):
    kargo = get_object_or_404(Kargo, pk=pk)
    if request.method == "POST":
        kargo.delete()
        messages.warning(request, "Kargo kaydı silindi.")
        return redirect('ana_sayfa')
    return render(request, 'kargo_sil_onay.html', {'kargo': kargo})