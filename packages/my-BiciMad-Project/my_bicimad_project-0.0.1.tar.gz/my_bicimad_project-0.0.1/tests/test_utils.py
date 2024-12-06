import pytest
import pandas as pd
from Bicimad.utils import (
    count_specific_unlock_lock_types, filter_regular_fleet, day_time,
    weekday_time, total_usage_day, total_usage_by_station_and_date,
    most_popular_stations, usage_from_most_popular_station
)

#Prueba para funciones auxiliares

def test_count_specific_unlock_lock_types():
    df = pd.DataFrame({'unlocktype': ['STATION', 'STATION', 'OTHER'], 'locktype': ['FREE', 'OTHER', 'FREE']})
    count = count_specific_unlock_lock_types(df)
    assert count == 1

def test_filter_regular_fleet():
    df = pd.DataFrame({'fleet': ['1', '2', '1']})
    filtered_df = filter_regular_fleet(df)
    assert len(filtered_df) == 2
    assert all(filtered_df['fleet'] == '1')

def test_day_time():
    df = pd.DataFrame({'trip_minutes': [60.0, 120.0, 180.0]}, index=pd.to_datetime(['2022-01-01', '2022-01-01', '2022-01-02']))
    total_hours_per_day = day_time(df)
    assert total_hours_per_day['2022-01-01'] == 3.0
    assert total_hours_per_day['2022-01-02'] == 3.0

def test_weekday_time():
    df = pd.DataFrame({'trip_minutes': [60, 120, 180]}, index=pd.to_datetime(['2022-01-03', '2022-01-04', '2022-01-05']))
    total_hours_per_weekday = weekday_time(df)
    assert total_hours_per_weekday['L'] == 1.0
    assert total_hours_per_weekday['M'] == 2.0
    assert total_hours_per_weekday['X'] == 3.0

def test_total_usage_day():
    df = pd.DataFrame(index=pd.to_datetime(['2022-01-01', '2022-01-01', '2022-01-02']))
    total_uses_per_day = total_usage_day(df)
    assert total_uses_per_day['2022-01-01'] == 2
    assert total_uses_per_day['2022-01-02'] == 1

def test_total_usage_by_station_and_date():
    df = pd.DataFrame({'station_unlock': [1, 1, 2]}, index=pd.to_datetime(['2022-01-01', '2022-01-01', '2022-01-02']))
    usage_by_station_and_date = total_usage_by_station_and_date(df)
    assert usage_by_station_and_date.loc['2022-01-01', 1] == 2
    assert usage_by_station_and_date.loc['2022-01-02', 2] == 1

def test_most_popular_stations():
    df = pd.DataFrame({'station_unlock': [1, 1, 2, 2, 2], 'address_unlock': ['addr1', 'addr1', 'addr2', 'addr2', 'addr2']})
    popular_stations = most_popular_stations(df)
    assert popular_stations == {'addr2'}

def test_usage_from_most_popular_station():
    df = pd.DataFrame({'station_unlock': [1, 1, 2, 2, 2]})
    usage = usage_from_most_popular_station(df)
    assert usage == 3

# Run tests
if __name__ == "__main__":
    pytest.main()
