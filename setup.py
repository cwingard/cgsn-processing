from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def version():
    with open('VERSION.txt') as f:
        return f.read().strip()


setup(
    name='cgsn_processing',
    version=version(),
    description=(
        'Collection of processing modules for converting JSON data '
        'from the OOI Endurance, Global and Pioneer moorings to NetCDF.'
    ),
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',
        'Topic :: Data Processing :: NetCDF :: ERDDAP :: Scientific :: OOI',
    ],
    keywords='OOI Endurance Global Pioneer moorings data processing',
    url='http://bitbucket.com/ooicgsn/cgsn-processing',
    author='Christopher Wingard',
    author_email='chris.wingard@oregonstate.edu',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'numpy',
        'scipy',
        'munch',
        'gsw',
        'pandas',
        'ppigrf',
        'netCDF4',
        'jinja2',
        'pytz',
        'requests',
        'xarray'
    ],
    include_package_data=True,
    zip_safe=False)
