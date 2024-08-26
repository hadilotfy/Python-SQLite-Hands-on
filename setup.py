from setuptools import setup, find_packages

setup(
    name='Python-SQLite-Hands-on',
    version='1.0.0',
    description='A python script that creates and add data to db, csv file and json files and generate report on the data.',
    author='Hadi Lotfy',
    author_email='hadi1lotfy@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hadilotfy/Python-SQLite-Hands-on.git',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas==2.2.2',
    ],
    python_requires='>=3.0',
    entry_points='''
        [console_scripts]
        hadi-etl-script=script:main
    ''',
)