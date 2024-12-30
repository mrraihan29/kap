from django.shortcuts import render

# Create your views here.

artikel_data ={
    1 : "KENAIKAN TARIF PPN DARI 11% MENJADI 12% YANG AKAN BERLAKU PADA JANUARI 2025",
    2 : "PENERAPAN PPH 21 TER",
    3 : "SPT TAHUNAN",
    4 : "PPN WAJIB PUNGUT BENDAHARAWAN NEGARA",
    5 : "PERBEDAAN PPh 26 dalam PPh 21/26 dan PPh 23/26",
    # 6 : "akua",
}

def list_artikel(request):
    return render(request, 'artikel/list_artikel.html', {'artikel_data': artikel_data})

def artikel_detail(request, artikel_id):
    judul = artikel_data.get(artikel_id, "Artikel tidak ditemukan")
    template_name = f'artikel/artikel_{artikel_id}.html'
    return render(request, template_name, {'judul': judul})
