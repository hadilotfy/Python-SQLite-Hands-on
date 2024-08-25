import sys

class DualStream:
    _instance = None
    
    def __new__(cls, file_name,is_print_report_to_screen):
        if cls._instance is None:
            cls._instance = super(DualStream, cls).__new__(cls)
            cls._instance._init(file_name,is_print_report_to_screen)
        return cls._instance

    def _init(self, file_name,is_print_report_to_screen):
        self.is_print_report_to_screen = is_print_report_to_screen
        # Save the original stdout
        self.original_stdout = sys.stdout
        # Open the file for writing
        self.file = open(file_name, 'w')
        # Redirect stdout to this instance
        sys.stdout = self
    
    def write(self, message):
        # Write to original stdout
        if self.is_print_report_to_screen:
            self.original_stdout.write(message)
        # Write to file
        self.file.write(message)
    
    def flush(self):
        # Flush original stdout
        if self.is_print_report_to_screen:
            self.original_stdout.flush()
        # Flush file
        self.file.flush()

    def close(self):
        # Restore the original stdout
        sys.stdout = self.original_stdout
        # Close the file
        self.file.close()
        # remove the singleton to be ready for initialization.
        type(self)._instance = None 
