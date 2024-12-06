import pytest
from happtiq_commons_google_cloud.logging_utils import is_cloud_function, setup_logging
from unittest.mock import MagicMock, patch
import os

@pytest.fixture
def empty_fixture():
    return

def test_is_cloud_function_with_k_service(monkeypatch):
    monkeypatch.setenv('K_SERVICE', 'test-service')
    assert is_cloud_function()

def test_is_cloud_function_without_k_service(monkeypatch):
    monkeypatch.delenv('K_SERVICE', raising=False)
    assert not is_cloud_function()


@patch('happtiq_commons_google_cloud.logging_utils.setup_cloud_function_logger')
@patch('happtiq_commons_google_cloud.logging_utils.is_cloud_function')
@patch('logging.basicConfig')
def test_setup_logging_cloud_function(mock_basic_config, mock_is_cloud_function, mock_setup_cloud_function_logger):
    mock_is_cloud_function.return_value = True
    mock_log_level = "DEBUG"

    setup_logging(log_level=mock_log_level)

    mock_is_cloud_function.assert_called_once()
    mock_setup_cloud_function_logger.assert_called_once_with(log_level=mock_log_level)
    mock_basic_config.assert_not_called()


@patch('happtiq_commons_google_cloud.logging_utils.setup_cloud_function_logger')
@patch('happtiq_commons_google_cloud.logging_utils.is_cloud_function')
@patch('logging.basicConfig')
def test_setup_logging_not_cloud_function(mock_basic_config, mock_is_cloud_function, mock_setup_cloud_function_logger):
    mock_is_cloud_function.return_value = False
    mock_log_level = "DEBUG"
    
    setup_logging(log_level=mock_log_level)

    mock_is_cloud_function.assert_called_once()
    mock_basic_config.assert_called_once_with(level=mock_log_level)
    mock_setup_cloud_function_logger.assert_not_called()

@patch('happtiq_commons_google_cloud.logging_utils.setup_cloud_function_logger')
@patch('happtiq_commons_google_cloud.logging_utils.is_cloud_function')
@patch('logging.basicConfig')
def test_setup_logging_not_cloud_function_default_log_level(mock_basic_config, mock_is_cloud_function, mock_setup_cloud_function_logger):
    mock_is_cloud_function.return_value = False
    
    setup_logging()

    mock_is_cloud_function.assert_called_once()
    mock_basic_config.assert_called_once_with(level="INFO")
    mock_setup_cloud_function_logger.assert_not_called()

@patch('happtiq_commons_google_cloud.logging_utils.setup_cloud_function_logger')
@patch('happtiq_commons_google_cloud.logging_utils.is_cloud_function')
@patch('logging.basicConfig')
def test_setup_logging_cloud_function_default_log_level(mock_basic_config, mock_is_cloud_function, mock_setup_cloud_function_logger):
    mock_is_cloud_function.return_value = True

    setup_logging()

    mock_is_cloud_function.assert_called_once()
    mock_setup_cloud_function_logger.assert_called_once_with(log_level="INFO")
    mock_basic_config.assert_not_called()
