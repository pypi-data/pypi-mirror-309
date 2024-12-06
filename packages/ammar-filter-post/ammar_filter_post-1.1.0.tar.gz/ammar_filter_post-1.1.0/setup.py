from setuptools import setup, find_packages

setup(
    name='ammar_filter_post',
    version='1.1.0',
    author='Ammar Abrahani',
    author_email='ammarabrahani@gmail.com',
    description='A package to retrieve and sort DynamoDB posts by likes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ammarabrahani@gmail.com/ammar_filter_post',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

