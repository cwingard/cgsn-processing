from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='cgsn_processing',
    version='0.1.1',
    description=(
        'Collection of processing modules for converting JSON data '
        'from the OOI Endurance, Global and Pioneer moorings to NetCDF.'
    ),
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Data Processing :: NetCDF :: ERDDAP :: Scientific :: OOI',
    ],
    keywords='OOI Endurance Global Pioneer moorings data processing',
    url='http://bitbucket.com/ooicgsn/cgsn-processing',
    author='Christopher Wingard',
    author_email='cwingard@coas.oregonstate.edu',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy >= 1.9.2',
        'scipy >= 0.15.1',
        'munch >= 2.1.0',
        'gsw >= 3.0.3',
        'pandas',
        'netCDF4',
        'jinja2',
        'pyseas',
        'pytz',
        'pyaxiom',
        'requests',
        'xarray'
    ],
    include_package_data=True,
    zip_safe=False)
