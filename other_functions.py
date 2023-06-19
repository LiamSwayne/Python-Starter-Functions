# prints the current program
def printProgram(delay=0):
    import time
    with open(__file__, 'r') as file:
        program_code = file.read()
        for char in program_code:
            print(char, end='', flush=True)
            time.sleep(delay)
