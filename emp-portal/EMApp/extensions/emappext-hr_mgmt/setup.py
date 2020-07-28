from setuptools import setup, find_packages
from os import path

# Path of the extension
here = path.abspath(path.dirname(__file__))


# Get description from Readme.md
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='emappext-hr_mgmt',  # Required
    version='1.0',
    description='Hr of Admin management packages registration for Employee Management App',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='git@github.com:gtkChop/EMPortal.git',
    author='Swaroop',
    author_email='swaroopbhak@gmail.com',
    classifiers=[  # Optional
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Topic : Employee Task Management App',
        'License : Open License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='Task Employee Task Management Management',
    packages=find_packages(
        exclude=['contrib', 'docs', 'tests'],
        include=['emappext.*']
    ),
    namespace_packages=['emappext'],
    python_requires='>=3.6',

    # All install packages should go on requirements.txt file
    install_requires=[
    ],
    extras_require={
    },
    package_data={
    },
    data_files=[
    ],

    message_extractors={
        'emappext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'emappcore', None),
            ('**/jinja2/**.html', 'emappcore', None),
            ('**/media/**', 'emappcore', None),
            ('**/static/**', 'emappcore', None),
        ],
    },

    # Entry Points
    entry_points={
        'emapp.register': [
            'hr_mgmt=emappext.hr_mgmt.register:EMAppHRManagementRegister'
        ],
    }
)
