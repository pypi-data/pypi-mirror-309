# İbb Açık Veri Portalı

İstanbul Büyükşehir Belediyesi'nin (İBB) açık veri portalından veri çekmek ve bu verileri analiz etmek için basit ve kullanışlı bir Python kütüphanesi.

## Özellikler
- İBB Açık Veri Portalı'ndan veri çekme
- Verileri pandas DataFrame veya JSON formatında dönüştürme
- Belirli veri setlerine hızlı erişim
- Kolay kurulum ve kullanım

## Kurulum
Projeyi pip ile kurabilirsiniz:

```bash
pip install ibb_acik_veri_portali
```

## Kullanım
Aşağıda kütüphanenin kullanımına ilişkin örnekler verilmiştir:

### Tüm Veri Setlerini JSON Formatında Çekmek
```python
from ibb_acik_veri_portali import json

# Tüm park verilerini JSON formatında al
data = json()
print(data)
```

### Belirli Bir Veri Setine Erişim
```python
from ibb_acik_veri_portali import json

# Belirli bir parkın detaylarını çek
park_id = 123
park_details = json(park_id=park_id)
print(park_details)
```

### Veriyi DataFrame Olarak Kullanmak
```python
from ibb_acik_veri_portali import dataframe

# Tüm park verilerini pandas DataFrame'e yükle
df = dataframe()
print(df.head())
```

### Series Formatında Veri Kullanımı
```python
from ibb_acik_veri_portali import series

# Belirli bir parkın detaylarını pandas Series olarak al
park_id = 123
park_series = series(park_id)
print(park_series)
```

## Gereksinimler
- Python 3.7 veya üstü
- Pandas
- Requests


## Lisans
Bu proje MIT lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına göz atabilirsiniz.

---

