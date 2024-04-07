import os
import pytest
from unittest.mock import patch, MagicMock
import src.app as app

# Test case 1: Process .tar.gz file
@patch('src.app.process_files.extract_gz')
@patch('os.remove')
def test_process_files_extract_gz(mock_remove, mock_extract_gz):
    file_path = 'file.tar.gz'

    # Call the function being tested
    app.process_files(file_path)

    # Verify that the test doubles were called
    mock_extract_gz.assert_called_once_with(file_path)
    mock_remove.assert_called_once_with(file_path)

# Test case 2: Process .csv file
@patch('src.app.process_files')
def test_process_files_csv(mock_process_files):
    file_path = 'file.csv'
    mock_process_files.return_value = file_path

    # Call the function being tested
    result = app.process_files(file_path)

    assert result == file_path

# Test case 3: Process .md file
@patch('src.app.process_files')
def test_process_files_markdown(mock_process_files):
    file_path = 'file.md'
    mock_process_files.return_value = file_path

    # Call the function being tested
    result = app.process_files(file_path)

    assert result == file_path

# Test case 4: Process .csv and .md files
@patch('src.app.create_tar_file')
@patch('src.app.create_pdfs')
@patch('src.app.modify_and_write_markdown')
@patch('src.app.read_csv_file')
def test_process_files_complete(mock_read_csv_file, mock_modify_and_write_markdown, mock_create_pdfs, mock_create_tar_file):
    mock_read_csv_file.return_value = MagicMock()
    mock_modify_and_write_markdown.return_value = MagicMock()
    mock_create_pdfs.return_value = MagicMock()
    mock_create_tar_file.return_value = MagicMock()

    # Call the function being tested
    app.process_files('dummy_file')

    # Verify that the test doubles were called
    mock_read_csv_file.assert_called_once()
    mock_modify_and_write_markdown.assert_called_once()
    mock_create_pdfs.assert_called_once()
    mock_create_tar_file.assert_called_once()

# Test case 5: Missing CSV file or Markdown template
@patch('src.app.process_files')
def test_process_files_missing_files(mock_process_files):
    mock_process_files.return_value = None

    # Call the function being tested
    result = app.process_files('dummy_file')

    assert result is None