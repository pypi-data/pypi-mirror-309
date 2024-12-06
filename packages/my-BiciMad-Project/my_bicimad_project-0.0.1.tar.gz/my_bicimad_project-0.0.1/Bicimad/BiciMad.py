import pandas as pd
from Bicimad import UrlEMT
from Bicimad.utils import count_specific_unlock_lock_types, filter_regular_fleet, day_time, weekday_time, total_usage_day, total_usage_by_station_and_date, most_popular_stations, usage_from_most_popular_station

class BiciMad:
    """
    Clase para gestionar y analizar los datos de uso del sistema Bicimad.
    """
    def __init__(self, month: int, year: int):
        """
        Inicializa una incia de BiciMad
            :param month: (int): El mes para el cual se obtendrán los datos (1-12).
            :param year: (int): Los últimos 2 dígitos del año para el cual se obtendrán los datos (21-23).
        """
        self._month = month
        self._year = year
        self._data = self.get_data(month, year)
        self._regular_fleet = filter_regular_fleet(self._data)

    @staticmethod
    def get_data(month: int, year: int) -> pd.DataFrame:
        """
        Obtine los datos de uso del sistema Bicimad para el mes y año especificados.
            :param month: (int): El mes para el cual se obtendrán los datos (1-12).
            :param year: (int): Los últimos 2 dígitos del año para el cual se obtendrán los datos (21-23).
        :returns:
            pd.DataFrame: un DataFrame con los datos de uso y las columnas especificadas.
        :raises:
            ConnectionError: Si no se puede conectar con el servidor de la EMT
        """
        # Seleccionar columnas a importar, convertir las fechas a datetime y establecer 'unlock_date' como índice
        url_emt = UrlEMT()
        csv_file = url_emt.get_csv(month, year)
        # Leer todas las columnas para verificar los nombres exactos
        df_full = pd.read_csv(csv_file, sep=';', low_memory=False) #low_memory para columnas con tipos de datos mixtos

        columns_to_import = ['idBike', 'fleet', 'trip_minutes', 'geolocation_unlock', 'address_unlock', 'unlock_date',
                            'locktype', 'unlocktype', 'geolocation_lock', 'address_lock', 'lock_date',
                            'station_unlock', 'unlock_station_name', 'station_lock', 'lock_station_name']
        # Renombrar columnas si es necesario
        if 'unlock_date' not in df_full.columns:
            for col in df_full.columns:
                if 'unlock' in col.lower() and 'date' in col.lower():
                    df_full.rename(columns={col: 'unlock_date'}, inplace=True)

        df = df_full.loc[:, columns_to_import]
        # Convertir las fechas a datetime y establecer 'unlock_date' como índice
        df.loc[:, 'unlock_date'] = pd.to_datetime(df.loc[:, 'unlock_date'])
        df.set_index('unlock_date', inplace=True)
        df = df.infer_objects()  #advertencia FutureWarning

        # llamar a la función clean() para limpiar y transformar el dataframe
        df = BiciMad.clean(df)

        return df

    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        """
            Realiza la limpieza y transformación del DataFrame.
            :arg:
                df (pd.DataFrame): el DataFrame a limpiar.
            :returns:
                pd.DataFrame: el DataFrame limpio.
            """
        df.dropna(how='all', inplace=True)
        # Cambiar el tipo de datos de las columnas especificadas
        columns_to_str = ['fleet', 'idBike', 'station_lock', 'station_unlock']
        df[columns_to_str] = df[columns_to_str].astype(str)
        df['fleet'] = df['fleet'].apply(lambda x: x.rstrip('.0') if isinstance(x, str) and x.endswith('.0') else x)
        df['idBike'] = df['idBike'].apply(lambda x: x.rstrip('.0') if isinstance(x, str) and x.endswith('.0') else x)
        df['station_lock'] = df['station_lock'].apply(lambda x: x.rstrip('.0') if isinstance(x, str) and x.endswith('.0') else x)
        df['station_unlock'] = df['station_unlock'].apply(lambda x: x.rstrip('.0') if isinstance(x, str) and x.endswith('.0') else x)

        return df

    @property
    def data(self) -> pd.DataFrame:
        """
        Devuelve los datos de uso del sistema BiciMad.
        :returns:
            pd.DataFrame: un DataFrame con los datos de uso.
        """
        return self._data

    def __str__(self) -> str:
        """
        Devuelve una representación de los datos de uso del DataFrame en cadena.
        :returns:
            str: representación en cadena del DataFrame.
        """
        return str(self._data)

    def resume(self) -> pd.Series:

        """
        Devuelve un resumen de las estadísticas de uso.
        :returns
            pd.Series: Un resumen de las estadísticas de uso.
        """
        total_uses = len(self._data)
        total_time = self._data['trip_minutes'].sum() / 60  # Convertir minutos a horas
        most_popular_station = self._data['station_lock'].mode()[0]
        uses_from_most_popular = self._data[self._data['station_lock'] == most_popular_station].shape[0]

        # utils - funciones auxiliares (C1 - C8)
        filtered_df = count_specific_unlock_lock_types(self._data)
        regular_fleet = filter_regular_fleet(self._data)
        total_hours_per_day = day_time(self._data)
        total_hours_per_weekday = weekday_time(self._data)
        total_uses_per_day = total_usage_day(self._data)
        usage_by_station_and_date = total_usage_by_station_and_date(self._data)
        popular_station_addresses = most_popular_stations(self._data)
        most_popular_station_usage = usage_from_most_popular_station(self._data)

        resume_data = {
            'year': self._year,
            'month': self._month,
            'total_uses': total_uses,
            'total_time': total_time,
            'most_popular_station': most_popular_station,
            'uses_from_most_popular': uses_from_most_popular,
            # utils - funciones auxiliares (C1 - C8)
            'filtered_df': filtered_df,
            'regular_fleet': regular_fleet,
            'total_hours_per_day': total_hours_per_day,
            'total_hours_per_weekday': total_hours_per_weekday,
            'total_uses_per_day': total_uses_per_day,
            'usage_by_station_and_date': usage_by_station_and_date,
            'popular_station_addresses': popular_station_addresses,
            'most_popular_station_usage': most_popular_station_usage
        }
        return pd.Series(resume_data)


"""
# Ejemplo de uso de la clase BiciMad
# Asumimos que el archivo CSV está disponible en la URL especificada en get_data

try:
    usos = BiciMad(month=2, year=23)
    df = usos.data
    print("Resumen de datos:")
    print(usos.resume())
except Exception as e:
    print("Error:", e)
"""
