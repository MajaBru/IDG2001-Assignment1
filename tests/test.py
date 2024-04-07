import os
import unittest
import src.app as app

class TestApp(unittest.TestCase):
    # Test case 1: Process .tar.gz file
    def test_process_files_extract_gz(self):
        file_path = 'file.tar.gz'
        extract_gz_called = False
        os.remove_called = False

        def extract_gz(file_path):
            nonlocal extract_gz_called
            extract_gz_called = True

        def remove(file_path):
            nonlocal os.remove_called
            os.remove_called = True

        # Replace the real os.remove and extract_gz functions with our test doubles
        os.remove = remove
        app.process_files.extract_gz = extract_gz

        # Call the function being tested
        app.process_files(file_path)

        # Verify that the test doubles were called
        self.assertTrue(extract_gz_called)
        self.assertTrue(os.remove_called)

    # Test case 2: Process .csv file
    def test_process_files_csv(self):
        file_path = 'file.csv'
        global CSV_FILE
        CSV_FILE = None

        app.process_files(file_path)

        self.assertEqual(CSV_FILE, file_path)

    # Test case 3: Process .md file
    def test_process_files_markdown(self):
        file_path = 'file.md'
        global MARKDOWN_TEMPLATE
        MARKDOWN_TEMPLATE = None

        app.process_files(file_path)

        self.assertEqual(MARKDOWN_TEMPLATE, file_path)

    # Test case 4: Process .csv and .md files
    def test_process_files_complete(self):
        global CSV_FILE
        global MARKDOWN_TEMPLATE
        CSV_FILE = 'file.csv'
        MARKDOWN_TEMPLATE = 'file.md'

        csv_data_called = False
        modify_and_write_markdown_called = False
        create_pdfs_called = False
        create_tar_file_called = False

        def create_pdfs():
            nonlocal create_pdfs_called
            create_pdfs_called = True

        def create_tar_file():
            nonlocal create_tar_file_called
            create_tar_file_called = True

        read_csv_file_original = read_csv_file
        modify_and_write_markdown_original = modify_and_write_markdown
        create_pdfs_original = create_pdfs
        create_tar_file_original = create_tar_file

        read_csv_file = read_csv_file_original
        modify_and_write_markdown = modify_and_write_markdown_original
        create_pdfs = create_pdfs_original
        create_tar_file = create_tar_file_original

        app.process_files('dummy_file')

        self.assertTrue(csv_data_called)
        self.assertTrue(modify_and_write_markdown_called)
        self.assertTrue(create_pdfs_called)
        self.assertTrue(create_tar_file_called)

    # Test case 5: Missing CSV file or Markdown template
    def test_process_files_missing_files(self):
        global CSV_FILE
        global MARKDOWN_TEMPLATE
        CSV_FILE = None
        MARKDOWN_TEMPLATE = None

        app.process_files('dummy_file')

        self.assertIsNone(CSV_FILE)
        self.assertIsNone(MARKDOWN_TEMPLATE)

if __name__ == '__main__':
    unittest.main()