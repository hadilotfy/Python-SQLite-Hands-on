"""
reports_main module
-------------------

    Main interface to use in script main function.
    Has functions that initialize reports and wraps printing logic 
    by using DualStreams class to move / copy standard output and 
    to a file.

methods:

    define_reports() -> list[ETLReport]
        Here we define needed reports that will be generated in runtime.

    print_reports_wrapper(reports:list[ETLReport],report_output_file:str,is_print_report_to_screen:bool)
        Here Standard Output is being manipulated so that print 
        function outputs to both standard output and a file

    print_reports(reports:list[ETLReport])
        Puts the general report template.

"""

from ..dualstream import DualStream
from .etl_report import ETLReport
from .records_count_report import RecordsCountReport
from .incomplete_records_report import IncompleteRecordsReport
from .sample_report import DatasetSampleReport
from .value_counts_report import ValuesCountsReport

def define_reports() -> list[ETLReport]:
    '''
    define_reports method

        define and initialize reports for the project.

    args:
        None
    
    returns:
        list[ETLReport]: 
            a list of ETLReport instances that is ready to be supplied with data
            and then be printed.
         

    '''
    reports = []
    
    count_rep = RecordsCountReport(description='Number of records in dataset')
    reports.append(count_rep)

    have_null_record_count_rep = IncompleteRecordsReport(description='Number of records with -at least- one null value')
    reports.append(have_null_record_count_rep)

    samples_rep = DatasetSampleReport(description='Sample of dataset',sample_count=5)
    reports.append(samples_rep)

    domains_counts_rep = ValuesCountsReport(column_name='email',
                description='Fequencies of email domains',
                preprocessing_func=lambda x: x.split('@')[1]
                )
    reports.append(domains_counts_rep)

    titles_counts_rep = ValuesCountsReport(column_name='title',
                description='Fequencies of titles', top_count= 3
                )
    reports.append(titles_counts_rep)
    
    return reports



def print_reports_wrapper(reports:list[ETLReport],report_output_file:str,is_print_report_to_screen:bool):
    '''
        Wrapper for print_reports method, to manipulate standard output 
        so that print() method outputs to both standard output and a file.

        args:
            reports: list[ETLReport]
                list of ETLReport instances which should 
                have been accumelated with data.

            report_output_file: str
                path to output report file.

            is_print_report_to_screen: bool
                whether to print to console or not.

        returns:
            None
    '''
    dual_stream = None
    try:
        # Create or get the singleton instance of DualStream
        dual_stream = DualStream(report_output_file,is_print_report_to_screen)

        # Any printing here will go to <report_output_file>
        #     and also to console if 'is_print_report_to_screen' is True.
        print_reports(reports)

    
    except Exception as e:
        print(f'Error printing_report_wrapper: {e}')
        print('exiting...')
        exit(1)
    finally:
        if dual_stream:
            # Restore the original stdout and close the stream
            dual_stream.close()

    

def print_reports(reports:list[ETLReport]):
    '''
    print_reports method
    --------------------
        =   defines the top-level report template, and calles print function 
            of ETLReport instances to add reports ouputs to this template.
        
        =   prints the full report to current standard output of the system.

    args:
        reports: list[ETLReport]
    
    returns:
        None

    
    '''
    num = len(reports)
    print('--------------------------------------------------------')        
    print(f'--------------------- {num} Reports ------------------------')
    for i in range(len(reports)):
        print(f'---------{i+1}/{num}---------')
        reports[i].print_report()
        print()
    print('--------------------------------------------------------')

