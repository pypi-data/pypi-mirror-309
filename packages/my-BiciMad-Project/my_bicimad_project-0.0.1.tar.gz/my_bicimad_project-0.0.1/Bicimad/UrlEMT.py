import re
import requests
import zipfile
from typing import Set, TextIO
from io import BytesIO, StringIO



class UrlEMT:
    """
    Clase para interactuar con los datos abiertos de EMT Madrid.
    """
    EMT = 'https://opendata.emtmadrid.es/'
    GENERAL = 'Datos-estaticos/Datos-generales-(1)'

    def __init__(self):
        """
        Inicializa una instancia de UrlEMT y selecciona las URLs válidas
        """
        self._valid_urls: Set[str] = self.select_valid_urls()

    @staticmethod
    def select_valid_urls() -> Set[str]:
        """
        Selecciona y devuelve un conjunto de URLs válidas.
        :return:
            Set[str]:  Un conjunto de URLs válidas.
        :raises:
            ConnectionError:  Si no se puede conectar con el servidor de EMT.
        """
        url = f'{UrlEMT.EMT}{UrlEMT.GENERAL}'
        response = requests.get(url)
        if not response.ok:
            raise ConnectionError('Error al conectar con el servidor de la EMT')
        html_text = response.text
        links = UrlEMT.get_links(html_text)
        valid_urls = {url for url in links if re.match(r'.*trips_\d{2}_\d{2}_[A-Za-z]+-csv\.aspx', url)}
        return valid_urls

    @staticmethod
    def get_links(html_text: str) -> Set[str]:
        """
        Extrae y devuelve todos los enlaces válidos desde el HTML proporcionado.
        :param
            html_text(str): El texto HTML desde el cual se extraen los enlaces

        :return
            Set[str]: Un conjunto de enlaces válidos.
        """
        pattern = re.compile(r'href="(.*?)"')
        links = set(re.findall(pattern, html_text))

        # Filtrar solo los enlaces completos y válidos
        base_url = 'https://opendata.emtmadrid.es'
        valid_links = {base_url + link for link in links if
                       'getattachment' in link and 'trips_' in link and link.endswith('-csv.aspx')}

        return valid_links

    def get_url(self, month: int, year: int) -> str:
        """
        Obtiene la URL válida para un mes y año específicos.
            :param month: (int).  El mes para el cual obtener la URL (1-12)
            :param year: (int). Los dos últimos dos dígitos del año para el cual obtener la URL (21-23)
        :return
            str: La URL válida para el mes y año especificados.
        :raises
            ValueError: Si el mes o año son inválidos.
        """
        if not (1 <= month <= 12):
            raise ValueError('Mes inválido. Debe estar entre 1 y 12.')
        if not (21 <= year <= 23):
            raise ValueError('Año inválido. Debe estar entre 21 y 23.')

        # Verificar si el mes y el año están dentro del rango válido
        if (year == 21 and month < 6) or (year == 23 and month > 2) or year < 21 or year > 23:
            raise ValueError("Mes y año fuera del rango válido. Deben estar entre junio '21 y febrero '23")

        month_str = f'{month:02d}'
        year_str = str(year)
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        month_name = months[month - 1]

        url_pattern = f'trips_{year_str}_{month_str}_{month_name}-csv.aspx'
        for url in self._valid_urls:
            if url_pattern in url:
                return url
        raise ValueError(f'No se encontró un enlace válido para {month_name} {year_str}')

    def get_csv(self, month: int, year: int) -> TextIO:
        """
        Descarga el archivo CSV para un mes y año específicos.

        :param month: (int). El mes para el cual descargar el archivo CSV (1-12)
        :param year: (int).  El año para el cual descargar el archivo CSV (21-23)
        :return
            TextIO: el contenido del archivo CSV.
        :raises
            ConnectionError: Si no se puede conectar con el servidor de la EMT.
        """
        url = self.get_url(month, year)
        response = requests.get(url)
        if not response.ok:
            raise ConnectionError('Error al conectar con el servidor de la EMT')

        # Manejar archivos ZIP
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            file_name = z.namelist()[0]
            with z.open(file_name) as csv_file:
                content = csv_file.read().decode('utf-8')
                return StringIO(content)



# Inicialización del objeto class UrlEMT
emt = UrlEMT()

#Ejemplo de uso de get_url y get_csv
try:
    url = emt.get_url(2, 23)
    print('URL:', url)
    csv_file = emt.get_csv(2, 23)
    print('CSV content:', csv_file.read())
except ValueError as e:
    print('Error:', e)
except ConnectionError as e:
    print('Error:', e)


