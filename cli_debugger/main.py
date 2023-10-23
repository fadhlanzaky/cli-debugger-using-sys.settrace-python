import functions
import inspect
import re

from debugger import start_debug
from util import clear_cli


def main():

    clear_cli()

    # a list to store all the breakpoints
    breakpoint_list = []

    # func name input
    function_name = input('function name: ')
    try:
        eval(f'functions.{function_name}')
    except Exception as e:
        if isinstance(e,AttributeError):
            # if function doesn't exist, stop
            print(f"function {function_name} not found in functions.py")
            return
    
    clear_cli()

    # parameters input
    print('add parameters manually? (y/n)')
    if input('> ').lower() == 'y':
        print("type(value). ex: int(2), str('hello world'), None")
        # create a dictionary of the parameters to be passed when executing the function
        func_args = {
                        item:eval(input(f"{item}: ")) 
                        for item in inspect.signature(eval(f'functions.{function_name}')).parameters.keys()
                    }
    else:
        print("make sure the function has default parameters")
        # create a dictionary of the parameters using its default
        func_args = {
                        item: (value.default if value.default is not inspect.Parameter.empty else None)
                        for item, value in inspect.signature(eval(f'functions.{function_name}')).parameters.items() 
                    }
        
    clear_cli()

    # breakpoints input
    print('add breakpoints? (y/n)')
    if input('> ').lower() == 'y':
        cnt = 1

        # the format must be {function_name} - {line number}
        print('{function name} - {line number}. ex: sample - 2')
        print(':q for quit')
        while True:
            bk_point = input(f"{cnt:<3}")
            if bk_point.lower().strip() == ':q':
                break
            if not re.match(r'\s*\w+\s*-\s*\d+\s*', bk_point):
                # if doesn't match the pattern, ignore it
                continue

            fn, ln = map(lambda x: x.strip(), bk_point.split('-'))
            # append the breakpoint to the list
            breakpoint_list.append((fn, int(ln)))
            cnt += 1

    clear_cli()

    # start debugging
    start_debug(breakpoint_list, eval(f'functions.{function_name}'), func_args)

if __name__ == '__main__':
    main()