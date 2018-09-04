from setuptools import setup, find_packages

setup(
    name='minidlna_exporter',
    version='0.1',
    url='https://github.com/dr1s/minidlna_exporter.py',
    author='dr1s',
    license='MIT',
    description='Export minidlna metrics for prometheus',
    install_requires=['prometheus_client', 'beautifulsoup4'],
    packages=find_packages(),
    include_package_data = True,
    entry_points={'console_scripts': ['minidlna_exporter=minidlna_exporter.minidlna_exporter:main']},
)
