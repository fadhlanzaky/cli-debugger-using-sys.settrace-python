import functions
import inspect
import sys

from util import clear_cli, FormatPrint

class DebuggerStop(Exception):
    """Custom exception for stopping execution"""
    pass

class DebuggerException(Exception):
    """Custom debugger exception"""
    pass

class Debugger(object):
    def __init__(self, breakpoint_list=[]) -> None:
        self.curr_cmd = None
        self.initial = True
        self.breakpoint_list = breakpoint_list
        self.format_print = FormatPrint()
        

    def trace_returns(self, frame, event, arg):
        """Handler that's executed when reaching return"""

        # only proceeds return event and exception
        if event == 'return':
            # continue to the next line as we do not care about return event
            return self.trace_lines
        elif event == 'exception':
            raise DebuggerException(self.format_print.fail(str(arg)))
        return 


    def trace_lines(self, frame, event, arg):
        """Handler that's executed each line"""

        # when it's not 'continue' return to controller
        if event == 'line' and self.curr_cmd != 'c':
            return self.controller(frame)
        elif event == 'exception':
            raise DebuggerException(self.format_print.fail(str(arg)))
        
        

    def trace_continue(self, frame, event, arg):
        """Handler that's executed to find breakpoints"""

        if event == 'exception':
            raise DebuggerException(self.format_print.fail(str(arg)))
        
        if self.breakpoint_list:
            # if breakpoint_list not empty, check if position exists in the list
            if (frame.f_code.co_name, frame.f_lineno) in self.breakpoint_list:
                return self.controller(frame)
        else:
            # if empty but initial call, go to the first line of the code
            if self.initial:
                print(self.format_print.header('START DEBUGGING'))
                self.initial = False
                return self.trace_lines

        if self.curr_cmd == 'o':
            # if step over, return the return callback
            return self.trace_returns
        elif self.curr_cmd == 'c':
            # if continue, keep searching the breakpoint until the end of the code
            return self.trace_continue
        
        # ignore 'def', go to the first line of the code immediately
        if frame.f_lineno == frame.f_code.co_firstlineno and self.curr_cmd == 'n':
            return self.trace_lines
        elif self.curr_cmd == 'n':
            return self.controller(frame)
        
        return self.trace_continue
        

    def controller(self, frame):
        """Directs user input to the appropriate handler"""

        # display the source code
        self.display(frame)
        self.curr_cmd = input('> ')
        clear_cli()

        # handlers are stored as string in this dictionary
        cont_map = {
            'n': "self.trace_lines",
            'o': "self.trace_lines",
            'c': "self.trace_continue",
            'q': "self._Debugger__stop()",
            'h': "self.display_help()",
            'v': "self.display_locals(frame)",
            'x': "self.run_expression(frame)"
        }
        trace = cont_map.get(str(self.curr_cmd))
        if not trace:
            # if input command doesn't exist in mapping, ignore
            return self.controller(frame)
        
        return eval(trace)


    def run_expression(self, frame):
        """Takes user input and execute it as a code using exec()"""

        print('write expression. :q for quit')
        expression = input('>> ')
        if expression == ':q':
            return self.controller(frame)
        else:
            try:
                # executing user input
                exec(expression,frame.f_globals,frame.f_locals)
            except Exception as e:
                print(str(e))
            
            self.run_expression(frame)
    

    def __stop(self):
        """Stopper"""

        raise DebuggerStop(self.format_print.warning('Execution Stopped'))
    

    @staticmethod
    def display_help():
        """Displays help messages"""

        help_message = [
                f"{'c':7}: Continue",
                f"{'h help':7}: Print this help message",
                f"{'n':7}: Step In",
                f"{'o':7}: Step Over",
                f"{'q':7}: Stop Execution",
                f"{'v':7}: Display Local Variables",
                f"{'x':7}: Evaluate Expressions",
                ]
        print(FormatPrint().underline('Help'))
        print('\n'.join(help_message))


    @staticmethod
    def display_locals(frame):
        """Displays local variables"""

        print(f"| {'var':10} | {'val':20} | {'':10} |")
        print('\n'.join([f"| {k:10} | {v:<20} | {'local':10} |" for k,v in frame.f_locals.items()]))


    @staticmethod
    def display(frame):
        """Displays source code"""

        # get the source code
        source_code = inspect.getsourcelines(frame.f_code)[0]

        if len(source_code) > 20:
            # sliding window for source code longer than 20 lines
            source_code = source_code[(frame.f_lineno-2):(frame.f_lineno + 18)]
            curr_line = 1
        else:
            curr_line = frame.f_lineno - frame.f_code.co_firstlineno

        source_code[curr_line] = FormatPrint().line(source_code[curr_line])
        print('-------------------------')
        print(''.join(source_code))


def start_debug(breakpoint_list, fn, kwargs):

    # start tracing
    sys.settrace(Debugger(breakpoint_list).trace_continue)
    
    # execute the function
    fn(**kwargs)
    
    print(FormatPrint().header('DEBUG ENDED'))
