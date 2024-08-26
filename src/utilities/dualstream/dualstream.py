""""
class DualStream - a Singleton class

handles redirection of standard output so that 
it prints to a file and to the console at the same time.

methods:
    __new__ (cls, file_name,is_print_report_to_screen)
    _init   (self, file_name,is_print_report_to_screen)
    write   (self, message)
    flush   (self)
    close   (self)

"""

import sys

class DualStream:
    
    _instance = None  # class variable that holds the singleton
    

    def __new__(cls, file_path,is_print_report_to_screen):
        """
        __new__ class function is called when a new instance is being created.

        if the singleton is already initialized, return it.
        if not , then initialize it and sent it back.


        args:
            filename: path to output file.
            is_print_report_to_screen: print to screen or not(just to the file).
        """
        if cls._instance is None:
            cls._instance = super(DualStream, cls).__new__(cls)
            cls._instance._init(file_path,is_print_report_to_screen)
        return cls._instance

    def _init(self, file_path,is_print_report_to_screen):
        """
        _init , the initializer which is called only if 
        
        """
        self.is_print_report_to_screen = is_print_report_to_screen
        # Save the original stdout
        self.original_stdout = sys.stdout
        # Open the file for writing
        self.file = open(file_path, 'w')
        # Redirect stdout to this instance
        sys.stdout = self
    
    def write(self, message):
        '''
        write method
            used to write message to the file [and to the console].

        args:
            message: str , the data to write to the file [and to the console].
        '''
        # Write to original stdout
        if self.is_print_report_to_screen:
            self.original_stdout.write(message)
        # Write to file
        self.file.write(message)
    
    def flush(self):
        """
        Flush
        flushes the output to the file and console.

        if used print it will call flush automatically.
        """
        # Flush original stdout
        if self.is_print_report_to_screen:
            self.original_stdout.flush()
        # Flush file
        self.file.flush()

    def close(self):
        """
        close
        closes the DualStream and return standard output to the original state 
        before initializing DualStream.
        
        """
        # Restore the original stdout
        sys.stdout = self.original_stdout
        # Close the file
        self.file.close()
        # remove the singleton to be ready for initialization.
        type(self)._instance = None 
