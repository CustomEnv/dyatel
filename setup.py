import os
import shutil

from dyatel import dyatel_version
from setuptools import setup

with open('README.md') as f:
    description = f.read()


pypi_name = 'dyatel-wrapper'
project_name = 'dyatel'
egg_name = pypi_name.replace('-', '_')


def cleanup():
    home_dir = os.getcwd()
    shutil.rmtree(f'{home_dir}/dist', ignore_errors=True)
    shutil.rmtree(f'{home_dir}/{egg_name}.egg-info', ignore_errors=True)

    print('Previous packages removed from local')


def get_packages(root_dir):
    all_dirs = [root_dir]

    for dirpath, dirnames, _ in os.walk(project_name):
        for dirname in dirnames:
            relative_path = os.path.relpath(os.path.join(dirpath, dirname), project_name)
            subdir = os.path.join(root_dir, relative_path).replace(os.path.sep, '.')
            if '__' not in subdir:
                all_dirs.append(subdir)

    print(f'Packages are: {all_dirs}')

    return all_dirs


cleanup()


setup(
    name=pypi_name,
    version=dyatel_version,
    url=f'https://github.com/EnvInc/{project_name}',
    packages=get_packages(project_name),
    install_requires=[
        'Appium-Python-Client>=2.1.2',
        'numpy>=1.18.1',
        'opencv-python>=4.5.5.62',
        'Pillow>=6.2.2',
        'playwright>=1.41.0',
        'selenium>=4.1.0',
        'scikit-image>=0.20.0',
    ],
    keywords='selenium appium playwright web_automation mobile_automation',
    description='Wrapper of Selenium, Appium and Playwright with single API',
    long_description=description,
    long_description_content_type='text/markdown',
    author_email='vladimir.podolyan64@gmail.com',
    author='Podolian Vladimir',
    project_urls={
        'Source': f'https://github.com/EnvInc/{project_name}',
        'Tracker': f'https://github.com/EnvInc/{project_name}/issues',
        'Documentation': f'https://{pypi_name}.readthedocs.io',
        'Changelog': f'https://github.com/EnvInc/{project_name}/blob/master/CHANGELOG.md'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing :: Acceptance',
        'License :: OSI Approved :: Apache Software License'
    ],
)
