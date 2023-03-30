from setuptools import setup

with open('README.md') as f:
    description = f.read()

setup(
    name='dyatel-wrapper',
    version='2.0.0',
    url='https://github.com/EnvInc/dyatel',
    packages=[
        'dyatel',
        'dyatel.base',
        'dyatel.mixins',
        'dyatel.dyatel_play',
        'dyatel.dyatel_sel',
        'dyatel.dyatel_sel.core',
        'dyatel.dyatel_sel.driver',
        'dyatel.dyatel_sel.elements',
        'dyatel.dyatel_sel.pages',
    ],
    install_requires=[
        'Appium-Python-Client>=2.1.2',
        'numpy>=1.18.1',
        'opencv-python==4.5.5.62',
        'Pillow>=6.2.2'
        'playwright>=1.30.0',
        'selenium>=4.1.0',
        'scikit-image>=0.17.1',
    ],
    keywords='selenium appium playwright web_automation mobile_automation',
    description='Wrapper of Selenium, Appium and Playwright with single API',
    long_description=description,
    long_description_content_type='text/markdown',
    author_email='vladimir.podolyan64@gmail.com',
    author='Podolian Vladimir',
    project_urls={
        'Source': 'https://github.com/EnvInc/dyatel',
        'Tracker': 'https://github.com/EnvInc/dyatel/issues',
        'Changelog': 'https://github.com/EnvInc/dyatel/blob/master/CHANGELOG.md'
    },
    classifiers=[
        'Development Status :: 2 - Beta',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing :: Acceptance',
        'License :: OSI Approved :: Apache Software License'
    ],
)
