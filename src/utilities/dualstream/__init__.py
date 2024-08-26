"""
dualstream package
------------------
Handle redirection of standard output so that 
it prints to a file and to the console at the same time.

    one module: 
        dualstream

    one class : 
        DualStream Singleton Class
"""


from .dualstream import DualStream

__all__=['DualStream']