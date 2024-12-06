from uuid import uuid4
from tempfile import NamedTemporaryFile
import os

class Storage:
    def __init__(self):
        self.temp_files = []  # List to keep track of temporary files
        self.tmp_dir = '/tmp/dimer'
        os.makedirs(self.tmp_dir, exist_ok=True)

    def get_temp_file_name_candidate(self, file_extension=''):
        return f'{self.tmp_dir}/dimer_{uuid4()}{file_extension}'

    def get_temporary_file(self, extension=''):
        temp_file = NamedTemporaryFile(prefix=f'dimer_', suffix=extension, dir=self.tmp_dir, delete=False)
        self.temp_files.append(temp_file)  # Track the temporary file
        return temp_file
    
    def get_temporary_files_directory(self):
        return self.tmp_dir

    def cleanup(self):
        """Delete all temporary files tracked by this Storage instance."""
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file.name)  # Remove the temporary file
                print(f'Temporary file deleted: {temp_file.name}')
            except OSError as e:
                print(f'Error deleting file {temp_file.name}: {e}')
        self.temp_files.clear()  # Clear the list after cleanup

# Example usage

default_storage = Storage()