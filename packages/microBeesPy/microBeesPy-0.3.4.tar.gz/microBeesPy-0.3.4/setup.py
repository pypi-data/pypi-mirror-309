from setuptools import find_packages, setup
import os

here = lambda *a: os.path.join(os.path.dirname(__file__), *a)

readme = open(here('README.md')).read()


setup(
    name='microBeesPy',
    packages=find_packages(),
    version='0.3.4',
    long_description=readme,
    keywords='microbees',
    long_description_content_type="text/markdown",
    description='microBees Python Library',
    author_email="developers@microbees.com",
    author='@microBeesTech',
    url='https://github.com/microBeesTech/pythonSDK/',
    license='MIT',
    install_requires=["aiohttp", "setuptools", "paho-mqtt"],
    zip_safe=False,
    platforms=["any"],
    python_requires='>=3.6',
    py_modules=["microBeesPy"],
)