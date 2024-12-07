# setup.py
from setuptools import setup, find_packages

setup(
    name='gns_helper',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Flask',                    # Web framework
        'Flask-JWT-Extended',       # JWT-based authentication
        'Pillow==9.5.0',            # Image processing (barcodes, labels)
        'pymysql',                  # MySQL database connector
        'dbutils',                  # Database connection pooling
        'pyyaml',                   # YAML parsing for configuration
        'requests',                 # HTTP requests for APIs (if needed)
    ],
    include_package_data=True,
    description='A package for common GNS functions',
    author='Komal Swami',
    author_email='komalsswami@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Minimum Python version
)
