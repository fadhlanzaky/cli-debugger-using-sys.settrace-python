## cli-debugger-using-sys.settrace-python
A simple CLI debugger utilizing sys.settrace()

## Start
* place the function you want to debug in `functions.py`
* run the debugger `python main.py`
* under function name question, type the name of the function
* next, add parameters (optional). Make sure the function has default params if you decide not to add
* next, add breakpoints (optional). The format is `{function name} - {line number}`

## Command
```sh
    Help
    c      : Continue
    h help : Print this help message
    n      : Step In
    o      : Step Over
    q      : Stop Execution
    v      : Display Local Variables
    x      : Evaluate Expressions
```
