"""Main file"""
from program import Program
from init import Init

def main():
    """Main function"""

    try:
        prog = Program()
    except:
        print("Something is wrong with your user name or password")
        exit(1)

    run = True
    while run:
        prog.consult_substitutes()
        prog.show_category()
        prog.show_product()
        prog.show_substitute()

        run = prog.continu()

ARG = None

try:
    INIT_DB = Init()
    ARG = INIT_DB.arg()

except AttributeError:
    pass

if __name__ == "__main__":
    if ARG is True:
        ARG
    else:
        main()
