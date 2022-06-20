from setuptools import setup, find_packages

with open('README.md') as f:
    description = f.read()

setup(
    name='dyatel',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Appium-Python-Client==2.1.2',
        'selenium==4.1.0',
        'playwright==1.22.0',
        'webdriver-manager==3.7.0',
    ],
    long_description=description,
)
