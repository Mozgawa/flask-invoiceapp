from setuptools import setup


setup(
    name='Invoice-parser',
    version='1.0',
    long_description=__doc__,
    packages=['invoice_parser'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
