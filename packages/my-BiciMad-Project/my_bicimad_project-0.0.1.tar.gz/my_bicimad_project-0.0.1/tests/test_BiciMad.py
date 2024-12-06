import pytest
import pandas as pd
from Bicimad import BiciMad
from Bicimad.utils import (
    count_specific_unlock_lock_types, filter_regular_fleet, day_time,
    weekday_time, total_usage_day, total_usage_by_station_and_date,
    most_popular_stations, usage_from_most_popular_station
)

def test_bicimad_initialization():
    # Create an instance of BiciMad
    bicimad = BiciMad(5, 22)

    # Test that the month and year are set correctly
    assert bicimad._month == 5
    assert bicimad._year == 22


def test_bicimad_get_data(mocker):
    # Predefined DataFrame with 'unlock_date' set as the index
    data = {
        'unlock_date': ['2022-05-01 00:01:36'],
        'idBike': [4911],
        'fleet': ['1'],
        'trip_minutes': [23.07],
        'geolocation_unlock': ["{'type:', 'Point', 'coordinates': [-3.6758383, 40.4239447]}"],
        'address_unlock': ['address1'],
        'locktype': ['Station'],
        'unlocktype': ['Station'],
        'geolocation_lock': ["{'type:', 'Point', 'coordinates': [-3.70239, 40.42059]}"],
        'address_lock': ['Calle Desengaño nº 1'],
        'lock_date': ['2022-05-01 00:09:26'],
        'station_unlock': [103],
        'unlock_station_name': ['98 - Plaza de Felipe II'],
        'station_lock': [219],
        'lock_station_name': ['211 - Desengaño']
    }
    index = pd.to_datetime(['2022-05-01 00:01:36'])
    df_mock = pd.DataFrame(data, index=index)
    df_mock.index.name = 'unlock_date'

    # Mock pandas read_csv to return the predefined DataFrame
    mocker.patch('pandas.read_csv', return_value=df_mock)

    # Mock filter_regular_fleet to return the predefined DataFrame
    mocker.patch('Bicimad.utils.filter_regular_fleet', return_value=df_mock)

    # Create an instance of BiciMad
    bicimad = BiciMad(5, 22)

    # Test the get_data method
    data = bicimad.get_data(5, 22)
    assert isinstance(data, pd.DataFrame)
    assert 'idBike' in data.columns
    assert 'fleet' in data.columns
    assert data.index.name == 'unlock_date'
    assert data.index[0] == pd.Timestamp('2022-05-01 00:01:36')
    assert data['idBike'].iloc[0] == '4911'
    assert data['fleet'].iloc[0] == '1'
    assert data['trip_minutes'].iloc[0] == 23.07
    assert data['geolocation_unlock'].iloc[0] == "{'type:', 'Point', 'coordinates': [-3.6758383, 40.4239447]}"
    assert data['locktype'].iloc[0] == 'Station'
    assert data['unlocktype'].iloc[0] == 'Station'
    assert data['geolocation_lock'].iloc[0] == "{'type:', 'Point', 'coordinates': [-3.70239, 40.42059]}"
    assert data['address_lock'].iloc[0] == 'Calle Desengaño nº 1'
    assert data['lock_date'].iloc[0] == '2022-05-01 00:09:26'
    assert data['station_unlock'].iloc[0] == '103'
    assert data['unlock_station_name'].iloc[0] == '98 - Plaza de Felipe II'
    assert data['station_lock'].iloc[0] == '219'
    assert data['lock_station_name'].iloc[0] == '211 - Desengaño'


def test_bicimad_clean():
    # Create a sample dataframe
    df = pd.DataFrame({
        'idBike': [1, None],
        'fleet': ['A', None],
        'trip_minutes': [10, None],
        'station_unlock': [1, None],
        'station_lock': [1, None],
    })

    # Clean the dataframe using the clean method
    cleaned_df = BiciMad.clean(df)

    # Test that the cleaned dataframe does not contain NaN values
    assert not cleaned_df.isnull().values.any()

def test_bicimad_resume(mocker):
    # Mock the methods and functions used in resume
    mocker.patch('Bicimad.utils.count_specific_unlock_lock_types', return_value=1)
    mocker.patch('Bicimad.utils.filter_regular_fleet', return_value=pd.DataFrame())
    mocker.patch('Bicimad.utils.day_time', return_value=pd.Series())
    mocker.patch('Bicimad.utils.weekday_time', return_value=pd.Series())
    mocker.patch('Bicimad.utils.total_usage_day', return_value=pd.Series())
    mocker.patch('Bicimad.utils.total_usage_by_station_and_date', return_value=pd.DataFrame())
    mocker.patch('Bicimad.utils.most_popular_stations', return_value=pd.Series())
    mocker.patch('Bicimad.utils.usage_from_most_popular_station', return_value=pd.Series())

    # Create an instance of BiciMad
    bicimad = BiciMad(5, 22)

    # Test the resume method
    resume = bicimad.resume()
    assert isinstance(resume, pd.Series)
    assert 'total_uses' in resume
    assert 'total_time' in resume

# Auxiliary function tests
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
