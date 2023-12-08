import pytest
from unittest.mock import Mock
from src.model.change_urls_to_presigned import change_urls_to_presigned
from bs4 import BeautifulSoup

@pytest.fixture
def sample_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="style.css">
        <script src="script.js"></script>
    </head>
    <body>
        <img src="image.png">
        <a href="page.html">Link</a>
        <a href="/absolute/link">Absolute Link</a>
        <a href="#anchor">Anchor Link</a>
    </body>
    </html>
    """

@pytest.fixture
def mock_s3_client():
    mock_s3 = Mock()
    mock_s3.generate_presigned_url.return_value = 'https://presigned.url'
    return mock_s3

@pytest.mark.unit
def test_change_html_links(sample_html, mock_s3_client):
    uuid = "test_uuid"
    aws_bucket = "test_bucket"
    url_changer = change_urls_to_presigned()
    modified_html = url_changer.change_html_links(sample_html, uuid, aws_bucket, mock_s3_client)
    soup = BeautifulSoup(modified_html, 'html.parser')
    assert soup.find('img')['src'] == 'https://presigned.url'
    anchor_tag = soup.find('a', href='https://presigned.url')
    assert anchor_tag is not None, "Anchor tag with updated href not found"
    assert soup.find('link', rel='stylesheet')['href'] == 'https://presigned.url'
    assert soup.find('script')['src'] == 'https://presigned.url'
    assert soup.find('a', href='/absolute/link')['href'] == '/absolute/link'
    assert soup.find('a', href='#anchor')['href'] == '#anchor'
    assert mock_s3_client.generate_presigned_url.call_count == 4

@pytest.mark.unit
def test_generate_presigned_url_for_path_with_absolute_url(mock_s3_client):
    uuid = "test_uuid"
    aws_bucket = "test_bucket"
    url_changer = change_urls_to_presigned()
    absolute_url = "http://example.com/image.png"
    result = url_changer.generate_presigned_url_for_path(absolute_url, f"src/book/{uuid}/", aws_bucket, mock_s3_client)
    assert result == absolute_url

@pytest.mark.unit  
def test_generate_presigned_url_for_path_relative_path(mock_s3_client):
    uuid = "test_uuid"
    aws_bucket = "test_bucket"
    url_changer = change_urls_to_presigned()
    relative_path = "relative/path/to/resource"
    expected_presigned_url = "https://presigned.url/relative/path/to/resource"
    mock_s3_client.generate_presigned_url.return_value = expected_presigned_url
    result = url_changer.generate_presigned_url_for_path(relative_path, f"src/book/{uuid}/", aws_bucket, mock_s3_client)
    assert result == expected_presigned_url

@pytest.mark.unit
def test_generate_presigned_url_exception_handling(mock_s3_client):
    uuid = "test_uuid"
    aws_bucket = "test_bucket"
    url_changer = change_urls_to_presigned()
    mock_s3_client.generate_presigned_url.side_effect = Exception("Test Exception")
    result = url_changer.generate_presigned_url(aws_bucket, "object_key", mock_s3_client)
    assert result is None
