
from .forms import ArtikelForm
from django.http import JsonResponse
from .models import Artikel
from django.utils.timezone import now
from django_ckeditor_5 import views as ckeditor_views
from urllib.parse import urlparse, parse_qs
import threading
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import json
from account.decorators import staff_required
from kap.utils import indo_date


def list_artikel(request):
    queryset = Artikel.objects.filter(deleted_at__isnull=True, published_at__isnull=False, published_at__lte=now(), draft_for__isnull=True).order_by('-published_at')
    data = queryset
    for artikel in data:
        artikel.published_at = indo_date(artikel.published_at, month_limit=3)
    
    return render(request, 'artikel/list_artikel.html', {'artikel_data': data, 'slider_data': data})

def detail_artikel(request, artikel_id):
    artikel = get_object_or_404(Artikel, id=artikel_id, deleted_at__isnull=True, draft_for__isnull=True)
    artikel.published_at = indo_date(artikel.published_at)
    return render(request, 'artikel/detail_artikel.html', {'data': artikel})

@staff_required
def list_artikel_admin(request):
    return render(request, 'artikel/list_artikel_admin.html')

@staff_required
def api_list_artikel_admin(request):
    current_time = now()
    queryset = Artikel.objects.filter(draft_for__isnull=True, deleted_at__isnull=True).order_by('-published_at')

    data = []
    for artikel in queryset:
        published = artikel.published_at is not None and artikel.published_at <= current_time
        draft = Artikel.objects.filter(draft_for=artikel, deleted_at__isnull=True).exists()
        unpublished = artikel.published_at is None
        publish_later = artikel.published_at is not None and artikel.published_at > current_time

        data.append({
            "id": artikel.id,
            "title": artikel.title,
            "description": artikel.description,
            "image": artikel.image.url if artikel.image else None,
            "created_at": artikel.created_at.isoformat(),
            "updated_at": artikel.updated_at.isoformat() if artikel.updated_at else None,
            "published_at": artikel.published_at.isoformat() if artikel.published_at else None,
            "deleted_at": artikel.deleted_at.isoformat() if artikel.deleted_at else None,
            "created_by": artikel.created_by.username if artikel.created_by else None,

            "published": published,
            "draft": draft,
            "unpublished": unpublished,
            "publish_later": publish_later,
        })

    return JsonResponse(data, safe=False)

@staff_required
def create_artikel(request):
    form = None
    if request.method == 'POST' and 'image' in request.FILES:
        # Handle form submission
        form = ArtikelForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the new article
            artikel = form.save(commit=False)
            artikel.created_by = request.user
            artikel.save()

            messages.success(request, "Artikel berhasil dibuat.")
            return redirect('edit_artikel', artikel_id=artikel.id)
    else:
        # Display the form
        form = ArtikelForm()
    return render(request, 'artikel/create_artikel.html', {'form': form})

@staff_required
def edit_artikel(request, artikel_id):
    original = get_object_or_404(Artikel, pk=artikel_id, draft_for__isnull=True, deleted_at__isnull=True)
    draft = Artikel.objects.filter(draft_for=original, deleted_at__isnull=True).first()
    instance = draft

    action = request.POST.get('action')

    # Logic untuk form instance
    if original.published_at is None and original.draft_for is None:
        # Artikel belum publish dan bukan draft → langsung edit original
        instance = original
    if not draft or action == 'discard_draft':
        if action == 'discard_draft' and draft:
            # Discard draft jika ada
            draft.deleted_at = now()
            draft.save()
            messages.success(request, "Draft berhasil dibuang.")
        # Kalau udah publish dan belum ada draft atau reset draft → buat draft kosong
        instance = Artikel(
            title=original.title,
            description=original.description,
            content=original.content,
            image=original.image,
            published_at=original.published_at,
            draft_for=original,
            created_by=request.user  # assuming request.user is required
        )

    if request.method == 'POST' and action in ['publish', 'draft', 'publish_now']:

        form = ArtikelForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            artikel = form.save(commit=False)
            artikel.updated_at = now()
            artikel.updated_by = request.user

            if action == 'publish' or action == 'publish_now':

                # Simpan ke original
                original.title = artikel.title
                original.description = artikel.description
                original.content = artikel.content
                if artikel.image:
                    original.image = artikel.image
                original.published_at = artikel.published_at
                original.updated_at = now()
                original.updated_by = request.user
                if action == 'publish_now':
                    # Force publish now
                    original.published_at = now()
                original.save()

                # Soft delete draft kalau ada
                if draft:
                    draft.deleted_at = now()
                    draft.save()

                messages.success(request, "Artikel berhasil dipublish.")
                return redirect('list_artikel_admin')

            elif action == 'draft':
                artikel.published_at = None  # force clear
                artikel.save()
                messages.success(request, "Draft berhasil disimpan.")
                return redirect('list_artikel_admin')
    else:
        form = ArtikelForm(instance=instance)

    return render(request, 'artikel/edit_artikel.html', {
        'form': form,
        'draft': instance != original,
        'now': now(),
        # 'artikel': instance
    })

@staff_required
def delete_artikel(request, artikel_id):
    artikel = get_object_or_404(Artikel, id=artikel_id)
    
    if request.method == 'GET':
        # Soft delete the article
        artikel.deleted_at = now()
        artikel.save()
        
        messages.success(request, "Artikel berhasil dihapus.")
        return redirect('list_artikel_admin')
    
    return redirect('list_artikel_admin')

@staff_required
def unpublish_artikel(request, artikel_id):
    artikel = get_object_or_404(Artikel, id=artikel_id)
    
    if request.method == 'GET':
        # Unpublish the article
        artikel.published_at = None
        artikel.save()
        
        messages.success(request, "Artikel berhasil di-unpublish.")
        return redirect('list_artikel_admin')
    
    return redirect('list_artikel_admin')

@staff_required
def upload_content_media(request):
    ret = ckeditor_views.upload_file(request)
    
    if ret.status_code == 200:
        data = json.loads(ret.content.decode())  # decode byte ke str, lalu parse JSON
        url = data.get('url', '')
        if url:
            query = parse_qs(urlparse(url).query)
            file_path = query.get('key', [''])[0]
            if file_path:
                # Create ContentMedia instance
                def create_content_media():
                    from artikel.models import ContentMedia, Artikel, CustomUser

                    referer = request.META.get('HTTP_REFERER', '')
                    last_segment = urlparse(referer).path.strip('/').split('/')[-1]
                    artikel_id = int(last_segment) if last_segment.isdigit() else None
                    artikel = Artikel.objects.filter(id=artikel_id).first()

                    user = request.user if request.user.is_authenticated else None

                    if artikel and user:
                        ContentMedia.objects.create(
                            artikel=artikel,
                            file=file_path,
                            created_by=user,
                        )

                threading.Thread(target=create_content_media).start()
    
    return ret

