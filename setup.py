import setuptools
import os

with open('README.rst', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


def get_packages(package):
    return [dirpath for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setuptools.setup(
    name='django-daylessdate',
    version='0.5',
    author='Michele Matera',
    author_email='mikimat2894@gmail.com',
    description='Provides a Django model and form fields for dates that do not include days.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/michelematera/django-daylessdate',
    project_urls={
        'Bug Tracker': 'https://github.com/michelematera/django-daylessdate/issues',
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
    packages=get_packages('djangodaylessdate'),
    package_data=get_package_data('djangodaylessdate'),
    python_requires='>=3.6',
)
