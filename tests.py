from functions.run_python_file import run_python_file
def main():
    separator = '\n' + '-' * 37
    result = run_python_file("calculator", "main.py")
    print('Showing results for: run_python_file("calculator", "main.py")')
    print(result)
    print(separator)
    result = run_python_file("calculator", "main.py", ["3 + 5"]) #(should run the calculator... which gives a kinda nasty rendered result)
    print('Showing results for: run_python_file("calculator", "main.py")')
    print(result)
    print(separator)
    
    result = run_python_file("calculator", "tests.py")
    print('Showing results for: run_python_file("calculator", "tests.py")')
    print(result)
    print(separator)
    
    result = run_python_file("calculator", "../main.py") #(this should return an error)
    print('Showing results for: run_python_file("calculator", "../main.py")')
    print(result)
    print(separator)

    result = run_python_file("calculator", "nonexistent.py") #(this should return an error)
    print('Showing results for: run_python_file("calculator", "nonexistent.py")')
    print(result)


if __name__ == "__main__":
    main()