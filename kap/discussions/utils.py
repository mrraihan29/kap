from django.utils import timezone

def relative_created_at(created_at):
    now = timezone.now()
    diff = now - created_at
    if diff.days == 0 and diff.seconds < 60:
        return f"{diff.seconds} detik"
    if diff.days == 0 and diff.seconds < 3600:
        minutes = diff.seconds // 60
        return f"{minutes} menit"
    if diff.days == 0 and diff.seconds < 86400:
        hours = diff.seconds // 3600
        return f"{hours} jam"
    if diff.days < 30:
        return f"{diff.days} hari"
    if diff.days < 365:
        months = diff.days // 30
        return f"{months} bulan"
    years = diff.days // 365
    return f"{years} tahun"
