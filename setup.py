from setuptools import setup, find_packages
from version import get_package_version

setup(
    name='route_optimization',
    version=get_package_version(),
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/shon-otmazgin/route_optimization',
    license='MIT License',
    author='Sapir Rubin;Shon Otmazgin',
    author_email='rubinsapir@gmail.com;shon711@gmail.com',
    description='route_optimization',
    python_requires='>=3.6',
    install_requires=[
        'pandas>=0.25.1',
        'numpy>=1.16.5'
    ]
)
