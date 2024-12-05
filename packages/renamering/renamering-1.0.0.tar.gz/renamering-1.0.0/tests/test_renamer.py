import os
import tempfile
from file_renamer.renamer import rename_files_and_replace_content

def test_rename_files_and_replace_content():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup: Create files and directories
        os.mkdir(os.path.join(tmpdir, "old_dir"))
        with open(os.path.join(tmpdir, "test_file.txt"), "w") as f:
            f.write("This is an old_word test.")
        with open(os.path.join(tmpdir, "old_dir", "nested_file.txt"), "w") as f:
            f.write("Nested old_word here.")

        # Run the function
        rename_files_and_replace_content(tmpdir, "old_word", "new_word")

        # Assertions: Check content replacement
        with open(os.path.join(tmpdir, "test_file.txt"), "r") as f:
            assert "new_word" in f.read()
        with open(os.path.join(tmpdir, "old_dir", "nested_file.txt"), "r") as f:
            assert "new_word" in f.read()

        # Assertions: Check renaming
        assert os.path.exists(os.path.join(tmpdir, "new_dir"))
