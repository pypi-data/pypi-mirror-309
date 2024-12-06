import requests as req
import pandas as pd

BASE_URL = 'https://api.ibb.gov.tr/ispark/'


def json(park_id: int = -1):
    """
    Belirtilen park ID'sine göre park verilerini JSON formatında döndürür.

    Args:
        park_id (int): İsteğe bağlı bir parametredir. Varsayılan olarak -1'dir.
                      -1 değeri tüm parkların verilerini alır.
                      Pozitif bir değer belirli bir parkın detaylarını getirir.

    Returns:
        dict or None: Park verilerini JSON formatında döndürür.
                      Eğer istek başarısız olursa `None` döner.

    Raises:
        HTTPError: API isteği başarısız olursa hata oluşabilir.
    """
    if park_id < 0:
        res = req.get(BASE_URL + 'Park')
        if res.status_code == 200:
            return res.json()
    else:
        res = req.get(BASE_URL + F'ParkDetay?id={park_id}')
        if res.status_code == 200:
            return res.json()[0]


def dataframe():
    """
    API'den tüm park verilerini alır ve bir pandas DataFrame olarak döndürür.

    Returns:
        pandas.DataFrame: Park verilerinden oluşan bir DataFrame.

    Raises:
        HTTPError: API isteği başarısız olursa hata oluşabilir.
    """
    return pd.read_json(BASE_URL + 'Park')


def series(park_id: int):
    """
    Belirli bir parkın verilerini pandas Series formatında döndürür.

    Args:
        park_id (int): Detaylarını almak istediğiniz parkın ID'si.

    Returns:
        pandas.Series: Belirli bir parkın verileri.

    Raises:
        KeyError: JSON verisinde beklenmeyen bir hata olursa.
    """
    return pd.Series(json(park_id))


if __name__ == "__main__":
    print(series(882))
