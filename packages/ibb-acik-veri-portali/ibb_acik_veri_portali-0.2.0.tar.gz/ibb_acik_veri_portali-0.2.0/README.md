# IBB Açık Veri Portalı

**IBB Açık Veri Portalı** projesi, İstanbul Büyükşehir Belediyesi'nin (İBB) Açık Veri Portalı üzerinden veri çekmek, analiz etmek ve kullanıcı dostu bir biçimde sunmak amacıyla geliştirilmiştir. Bu paket, veri çekme ve işleme işlemlerini kolaylaştırarak veri bilimciler, araştırmacılar ve geliştiriciler için güçlü bir araç seti sunar.

## Özellikler

- Belirli bir `park_id`'ye göre park verilerini JSON formatında getirme.
- İBB'nin park verilerini bir pandas `DataFrame` nesnesi olarak dönüştürme.
- Tek bir park verisini pandas `Series` formatında sunma.
- Kolay ve hızlı API bağlantıları.

## Kurulum

Projenizi `PyPI` üzerinden yükleyebilirsiniz:

```bash
pip install ibb-acik-veri-portali
```

## Kullanım

### Temel Kullanım

```
from ibb_acik_veri_portali import json, dataframe, series

# Tüm park verilerini çekme
tum_parklar = json()
print(tum_parklar)

# Belirli bir parkın detayları
park_detayi = json(park_id=1)
print(park_detayi)

# Park verilerini pandas DataFrame olarak çekme
df = dataframe()
print(df.head())

# Tek bir parkı pandas Series formatında çekme
park_series = series(park_id=1)
print(park_series)
```

## Bağımlılıklar

- `pandas`
- `requests`

Bu bağımlılıkları projenizle birlikte kurabilirsiniz:

```bash
pip install pandas requests
```

## Katkıda Bulunma

Katkıda bulunmak için lütfen bir [issue](https://github.com/kullanici/ibb-acik-veri-portali/issues) oluşturun veya bir pull request gönderin.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına göz atabilirsiniz.

## İletişim

Sorularınız veya önerileriniz için [e-posta adresiniz] üzerinden bizimle iletişime geçebilirsiniz.