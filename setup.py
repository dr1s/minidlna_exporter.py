from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='minidlna_exporter',
    version='0.1.1',
    url='https://github.com/dr1s/minidlna_exporter.py',
    author='dr1s',
    license='MIT',
    description='Export minidlna metrics for prometheus',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['prometheus_client', 'beautifulsoup4'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts':
        ['minidlna_exporter=minidlna_exporter.minidlna_exporter:main']
    },
)
