MONTHS = {
    'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
    'April': 'April', 'May': 'Mei', 'June': 'Juni',
    'July': 'Juli', 'August': 'Agustus', 'September': 'September',
    'October': 'Oktober', 'November': 'November', 'December': 'Desember'
}

def indo_date(value, fmt='%d %B %Y', month_limit=10):
    if not value:
        return ''
    eng_date = value.strftime(fmt)
    for en, idn in MONTHS.items():
        eng_date = eng_date.replace(en, idn[:month_limit])
    return eng_date