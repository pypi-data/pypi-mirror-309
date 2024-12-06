import requests as req
import pandas as pd

BASE_URL = 'https://api.ibb.gov.tr/ispark/'


def json(park_id: int = -1):
    """
    Belirtilen park ID'sine göre park verilerini JSON formatında döndüren fonksiyon.

    Args:
        park_id (int): Park ID'si. Varsayılan değer -1'dir.
                       -1 verilirse tüm parkların verisi döner.

    Returns:
        dict: Tek bir parkın detayları için JSON formatında veri döner.
              Eğer park_id belirtilmezse, tüm parkların listesini içeren JSON döner.
              Talep başarılı değilse, hiçbir değer dönmez.
    """
    if park_id < 0:
        res = req.get(BASE_URL + 'Park')
        if res.status_code == 200:
            return res.json()
    else:
        res = req.get(BASE_URL + f'ParkDetay?id={park_id}')
        if res.status_code == 200:
            return res.json()[0]


def dataframe():
    """
    API'den park verilerini çekerek bir DataFrame döndüren fonksiyon.

    Returns:
        pd.DataFrame: API'den çekilen park verilerinden oluşturulan bir pandas DataFrame.
    """
    return pd.read_json(BASE_URL + 'Park')


def series(park_id: int):
    """
    Belirtilen park ID'sine göre tek bir parkın detaylarını pandas Series olarak döndüren fonksiyon.

    Args:
        park_id (int): Park ID'si.

    Returns:
        pd.Series: Belirtilen parkın detaylarını içeren bir pandas Series objesi.
    """
    return pd.Series(json(park_id))


if __name__ == "__main__":
    print(series(882))
