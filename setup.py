from setuptools import setup, find_packages

setup(
    name='hadi-etl',
    version='2.0.0',
    description='A python script that creates and add data to db, csv file and json files and generate report on the data.',
    author='Hadi Lotfy',
    author_email='hadi1lotfy@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hadilotfy/Python-SQLite-Hands-on.git',
    install_requires=[
        'pandas==2.2.2',
        'tabulate==0.9.0'
    ],
    packages=find_packages(where='src'),
    package_dir={ '':'src' },
    py_modules=["script"],
    python_requires='>=3.0',
    entry_points={
        'console_scripts': 'hadi-etl-main=script:main'
    }
    ,
)