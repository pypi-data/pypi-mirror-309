from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as file:
        read_me = file.read()
    return read_me


setup(
    name='robotframework-awslibrary',
    version='0.0.1',
    author='Vinicius Henrique Especoto',
    description='A python package to create test cases for AWS services using Robot Framework',
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords='robotframework testing testautomation aws boto3',
    url='https://github.com/Hespius/robotframework-awslibrary',
    license='MIT Licence',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['boto3>=1.35.62', 'robotframework>=7.1.1', 'robotframework-pythonlibcore>=4.4.1'],
)