from functions.get_file_content import get_file_content
def main():
   text = get_file_content("calculator", "main.py")
   print(text)
#    print(f"main.py content length: {len(text)}")
   text = get_file_content("calculator", "pkg/calculator.py")
   print(text)
#    print(f"main.py content length: {len(text)}")
   text = get_file_content("calculator", "/bin/cat")
   print(text)
#    print(f"main.py content length: {len(text)}")
   text = get_file_content("calculator", "pkg/does_not_exist.py")
   print(text)
#    print(f"main.py content length: {len(text)}")
if __name__ == "__main__":
    main()