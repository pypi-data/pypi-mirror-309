"""
Setup file for the duino_vscode_settings module.
"""

from pathlib import Path
import sys

if sys.version_info < (3, 9):
    print('duino_vscode_settings requires Python 3.9 or newer.')
    sys.exit(1)

# pylint: disable=wrong-import-position
from setuptools import setup
from duino_vscode_settings.version import __version__

here = Path(__file__).parent
long_description = (here / "README.md").read_text()

setup(
    name='duino_vscode_settings',
    version=__version__,
    author='Dave Hylands',
    author_email='dhylands@gmail.com',
    description=('A tool for creating VSCode c_cpp_properties.json files.'),
    license='MIT',
    keywords='cmd cli arduino',
    url='https://github.com/dhylands/duino_vscode_settings',
    download_url=
    f'https://github.com/dhylands/duino_vscode_settings/shell/tarball/v{__version__}',
    packages=['duino_vscode_settings'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Shells',
        'Topic :: Terminals :: Serial',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'make-vscode-settings=duino_vscode_settings.duino_vscode_settings:main'
        ],
    },
)
