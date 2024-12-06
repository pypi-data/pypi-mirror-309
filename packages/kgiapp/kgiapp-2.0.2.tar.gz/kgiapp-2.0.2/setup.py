
import os
from setuptools import setup, find_packages, Distribution
# from Cython.Build import cythonize

dir_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(dir_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(self):
        return True


setup(
    name='kgiapp',
    # ext_modules = cythonize(module_list='kgiapp/*/*.py', exclude='kgiapp/*/__init__.py', compiler_directives={'language_level': sys.version_info[0]}),
    version='2.0.2',
    description='Python client for send order to KGI Securities.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Leo Wu',
    author_email='phymach@gmail.com',
    url='https://github.com/phymach',
    license='MIT',
    install_requires=[
        'pythonnet>3',
        'pandas',
        'psutil',
        'pywin32',
        'pyyaml'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    platforms=['Windows'],
    python_requires='>=3.11',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', '.vscode']),
    include_package_data=True,
    scripts=[],
    keywords=['stock', 'futures', 'option', 'TWSE', 'TPEX', 'TAIFEX'],
    distclass=BinaryDistribution,
)
