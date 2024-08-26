"""
Report Module
    Generate Reports based on Pandas DataFrame

methods:
    generate_report_wrapper(data:pd.DataFrame,report_output_file:str,is_print_report_to_screen:bool)
    generate_report(data:pd.DataFrame)
"""



from .dualstream import DualStream
import pandas as pd

def generate_report_wrapper(data:pd.DataFrame,report_output_file:str,is_print_report_to_screen:bool):
    '''
        Wrapper for generate report method, to edit standard output so that it outputs
        to both standard output and to a file.

        args:
            data: pandas.DataFrame, the data to generate report based on.
            report_output_file: str, path to output report file.
            is_print_report_to_screen: bool, whether to print to console or not.

        returns:
            None
    '''
    dual_stream = None
    try:
        # Create or get the singleton instance of DualStream
        dual_stream = DualStream(report_output_file,is_print_report_to_screen)

        # Any printing here will go to <report_output_file>
        #     and also to console if 'is_print_report_to_screen' is True.
        generate_report(data)

    
    except Exception as e:
        print(f'Error Writing Report: {e}')
        print('exiting...')
        exit(1)
    finally:
        if dual_stream:
            # Restore the original stdout and close the stream
            dual_stream.close()

def generate_report(data:pd.DataFrame):
    '''
        Generate report based on passed DataFrame object.

        args:
            data: Pandas.DataFrame, the data to build report based on.

        returns:
            None
    
    '''
    print(' Report')
    print('--------------------------------------------------')
    
    # 1. Total number of records.
    data_length = len(data)
    print('1.Number of records in dataset: ',data_length)

    # 2. Sample of 5 rows
    print('2.Sample of 5 rows:-')

    # sample_count = 5 if 5 < len(data) else len(data)
    # print(data.sample(n=sample_count))  # ,random_state=2 

    # print(data.sample(n=5,replace=True)) # get 5 rows even if length is less than 5.

    # 3. Other insights
    print('3.Insights on data:-')

    # 3.1   Top used email provider.
    print('  3.1 top 3 used email domains with counts:-')
    data['domain'] = data['email'].apply(lambda x: x.split('@')[1])  # Extract the domain part from the email
    domain_counts = data['domain'].value_counts()  # Count the frequency of each domain
    top_3_domains = domain_counts.head(3)  # Get the top 3 most frequent domains
    formatted_view = [f"{' ' * 4} #{row[1]} {row[0]}" for row in top_3_domains.items()]  # paddding and formating
    for line in formatted_view:
        print(line)

    # 3.2   3 Most frequently occurring titles.
    print('  3.2 top 3 assigned titles with counts:-')
    top_3_titles = data['title'].value_counts().head(3)  # Get the top 3 most frequent 'Titles'
    formatted_view = [f"{' ' * 4} #{row[1]} {row[0]}" for row in top_3_titles.items()]   # paddding and formating
    for line in formatted_view:
        print(line)

    # 3.3   Count of incomplete records.
    print('  3.3 Count of incomplete records: ', end='')
    incomplete_records = data.isnull().any(axis=1).sum()
    print(incomplete_records)

    print('--------------------------------------------------')
    