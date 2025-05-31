BULAN = {
    'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
    'April': 'April', 'May': 'Mei', 'June': 'Juni',
    'July': 'Juli', 'August': 'Agustus', 'September': 'September',
    'October': 'Oktober', 'November': 'November', 'December': 'Desember'
}
def indo_date(value, fmt='%d %B %Y'):
    if not value:
        return ''
    eng_date = value.strftime(fmt)
    for en, idn in BULAN.items():
        eng_date = eng_date.replace(en, idn)
    return eng_date