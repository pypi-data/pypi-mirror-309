import pytest
from unittest.mock import patch, Mock
from io import BytesIO
import zipfile
from Bicimad import UrlEMT


def test_select_valid_urls(mocker):
    # Mock the requests.get method
    mock_response = Mock()
    mock_response.ok= True
    mock_response.text = '<a href="/getattachment/trips_21_06_June-csv.aspx">Link</a>'
    mocker.patch('requests.get', return_value=mock_response)

    valid_urls = UrlEMT.select_valid_urls()
    assert len(valid_urls) == 1
    assert 'https://opendata.emtmadrid.es/getattachment/trips_21_06_June-csv.aspx' in valid_urls


def test_get_links():
    html_text = '<a href="/getattachment/trips_21_06_June-csv.aspx">Link</a>'
    expected_links = {'https://opendata.emtmadrid.es/getattachment/trips_21_06_June-csv.aspx'}
    assert UrlEMT.get_links(html_text) == expected_links


def test_get_url():
    url_emt = UrlEMT()
    url_emt._valid_urls = {'https://opendata.emtmadrid.es/getattachment/trips_21_06_June-csv.aspx'}

    url = url_emt.get_url(6, 21)
    assert url == 'https://opendata.emtmadrid.es/getattachment/trips_21_06_June-csv.aspx'


def test_get_url_invalid_month():
    url_emt = UrlEMT()
    with pytest.raises(ValueError, match='Mes inválido. Debe estar entre 1 y 12.'):
        url_emt.get_url(13, 21)


def test_get_url_invalid_year():
    url_emt = UrlEMT()
    with pytest.raises(ValueError, match="Año inválido. Debe estar entre 21 y 23."):
        url_emt.get_url(6, 24)


def test_get_csv(mocker):
    # Mock the requests.get method
    html_content = '<a href="/getattachment/trips_21_06_June-csv.aspx">Link</a>'
    mock_response = Mock()
    mock_response.ok = True
    mock_response.text = html_content

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        zf.writestr('test.csv', 'idBike,fleet,trip_minutes\n1,A,10')
    zip_buffer.seek(0)
    mock_response.content = zip_buffer.getvalue()

    mocker.patch('requests.get', return_value=mock_response)

    url_emt = UrlEMT()
    url_emt._valid_urls = {'https://opendata.emtmadrid.es/getattachment/trips_21_06_June-csv.aspx'}

    csv_file = url_emt.get_csv(6, 21)
    content = csv_file.read()
    assert 'idBike,fleet,trip_minutes\n1,A,10' in content


# Run tests
if __name__ == "__main__":
    pytest.main()


