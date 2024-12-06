import pandas as pd

from pandas.core.interchange.dataframe_protocol import DataFrame


# c1 - calcula el número de entradas donde Unlocktype es STATION y locktype es FREE
def count_specific_unlock_lock_types(df: pd.DataFrame) -> int:
    filtered_df = df[(df['unlocktype'] == 'STATION') & (df['locktype'] == 'FREE')].shape[0]
    return filtered_df

#c2 - selecciona bicicletas del tipo de flota '1' y regresa un nuevo dataframe
def filter_regular_fleet(df: pd.DataFrame) -> pd.DataFrame:
    regular_fleet = df[df['fleet'] == '1'].copy()
    return regular_fleet

# c3 - calcula las horas de uso de bicicleta por día del mes
def day_time(df: pd.DataFrame) -> pd.Series:
     df.index = pd.to_datetime(df.index)
     # convertir el valor en 'trip_minutes' a horas
     df['trip_duration'] = df['trip_minutes'] / 60
     # Agrupar por la fecha en el índice y encontrar el total de horas
     total_hours_per_day = df.groupby(df.index.date)['trip_duration'].sum()
     total_hours_per_day = total_hours_per_day.round(2)
     total_hours_per_day.index = total_hours_per_day.index.astype(str)
     return total_hours_per_day

# c4 - calcula las horas totales de uso de bicicletas por día de la semana
def weekday_time(df: pd.DataFrame) -> pd.Series:
    df.index = pd.to_datetime(df.index)
    df['trip_minutes'] = df['trip_minutes'] / 60  # convertir total en horas
    days = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}  # guía días de la semana
    df['weekday'] = df.index.weekday.map(days)
    total_hours_per_weekday = df.groupby('weekday')['trip_minutes'].sum()
    total_hours_per_weekday = total_hours_per_weekday.round(2)
    ordered_days = ['D', 'L', 'M', 'X', 'J', 'V', 'S']
    total_hours_per_weekday = total_hours_per_weekday.reindex(ordered_days)
    return total_hours_per_weekday

#c5 - calcula el No. total de usos de bicicleta por día del mes
def total_usage_day(df: pd.DataFrame) -> pd.Series:
     df.index = pd.to_datetime(df.index)
     total_uses_per_day = df.groupby(df.index.date).size()
     total_uses_per_day.index = total_uses_per_day.index.astype(str)
     return total_uses_per_day

# c6 - calcula el total de usos por fecha y estación
def total_usage_by_station_and_date(df: pd.DataFrame) -> pd.DataFrame:
    df.index = pd.to_datetime(df.index)
    usage_by_station_and_date = df.groupby([pd.Grouper(freq='1D'), 'station_unlock']).size()
    return usage_by_station_and_date

#c7 - averigua la dirección de estaciones de desbloqueo que a lo largo del mes han tenido un mayor número de viajes
def most_popular_stations(df: pd.DataFrame) -> set:
    df.index = pd.to_datetime(df.index)
    station_counts = df.groupby('station_unlock').size()
    max_trips = station_counts.max()
    most_popular_stations = station_counts[station_counts == max_trips].index.tolist()
    popular_station_addresses = df[df['station_unlock'].isin(most_popular_stations)]['address_unlock'].unique()
    return set(popular_station_addresses)


# c8 - calcula el No. total de usos de la estación más popular
def usage_from_most_popular_station(df: pd.DataFrame) -> int:
    df.index = pd.to_datetime(df.index)
    station_counts = df.groupby('station_unlock').size()
    max_trips_station = station_counts.idxmax()
    most_popular_station_usage = station_counts[max_trips_station]
    return most_popular_station_usage


