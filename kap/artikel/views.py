from django.shortcuts import render

# Create your views here.

artikel_data ={
    1 : "Penandatanan MOU antara Indonesia dan Malaysia",
    2 : "MU",
    3 : "MC",
    4 : "Artis",
    5 : "Menang",
    6 : "akua",
}

def list_artikel(request):
    return render(request, 'artikel/list_artikel.html', {'artikel_data': artikel_data})

def artikel_detail(request, artikel_id):
    judul = artikel_data.get(artikel_id, "Artikel tidak ditemukan")
    template_name = f'artikel/artikel_{artikel_id}.html'
    return render(request, template_name, {'judul': judul})
