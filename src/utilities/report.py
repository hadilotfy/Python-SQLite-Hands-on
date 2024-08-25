import sys
from .dualstream import DualStream

def generate_report_wrapper(data,report_output_file,is_print_report_to_screen):

    # Create or get the singleton instance of DualStream
    dual_stream = DualStream(report_output_file,is_print_report_to_screen)

    # Any printing here will go to <report_output_file>
    #     and also to console if 'is_print_report_to_screen' is True.
    generate_report(data)

    # Restore the original stdout and close the stream
    dual_stream.close()


def generate_report(data):
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
    top_3_domains = domain_counts.head(3).add_prefix('         ')  # Get the top 3 most frequent domains
    print(top_3_domains.to_string())

    # 3.2   3 Most frequently occurring titles.
    print('  3.2 top 3 assigned titles with counts:-')
    top_3_titles = data['title'].value_counts().head(3).add_prefix('         ')
    print(top_3_titles.to_string())

    # 3.3   Count of incomplete records.
    print('  3.3 Count of incomplete records: ', end='')
    incomplete_records = data.isnull().any(axis=1).sum()
    print(incomplete_records)
