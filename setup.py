from setuptools import setup


with open('README.md') as f:
    description = f.read()

setup(
    name='dyatel-wrapper',
    version='1.0.3',
    url='https://github.com/EnvInc/dyatel',
    packages=[
        'dyatel',
        'dyatel.base',
        'dyatel.dyatel_play',
        'dyatel.dyatel_sel',
        'dyatel.dyatel_sel.core',
        'dyatel.dyatel_sel.driver',
        'dyatel.dyatel_sel.elements',
        'dyatel.dyatel_sel.pages',
    ],
    install_requires=[
        'Appium-Python-Client==2.1.2',
        'selenium==4.1.0',
        'playwright==1.22.0',
        'webdriver-manager==3.7.0',
        'Pillow==9.1.1'
    ],
    keywords='selenium appium playwright web_automation mobile_automation',
    description='Wrapper of Selenium, Appium, Playwright',
    long_description=description,
    long_description_content_type="text/markdown",
    author_email="vladimir.podolyan64@gmail.com",
    author='Podolian Vladimir',
    project_urls={
        "Source": "https://github.com/EnvInc/dyatel",
        "Tracker": "https://github.com/EnvInc/dyatel/issues",
    },
)
