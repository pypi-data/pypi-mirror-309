# another_project.py
import time

from codealchemy import code_execution_time


@code_execution_time
def example_function():
    time.sleep(2)
    print("Function executed")


example_function()
