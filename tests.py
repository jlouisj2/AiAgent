print("--- Boots' Test Marker ---")
from functions.get_files_content import get_file_content

def run_tests():
    print("Reading main.py:")
    print(get_file_content("calculator", "main.py"), "\n")

    print("Reading calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"), "\n")

    print("Reading /bin/cat (should fail):")
    print(get_file_content("calculator", "/bin/cat"), "\n")

    print("Reading missing file (should fail):")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    run_tests()
