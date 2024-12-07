from setuptools import setup, find_packages

setup(
    name='database_setup',
    version='0.0.3',
    description='Database setup utilities with configuration handling',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='Komal Swami',
    author_email='komal@neudeep.in',
    packages=find_packages(),
    install_requires=[
        'pymysql',
        'dbutils',
        'PyYAML',
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)