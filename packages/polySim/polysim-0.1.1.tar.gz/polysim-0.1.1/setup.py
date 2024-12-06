from setuptools import setup, Extension
import numpy as np
import sys

# Check if Windows platform
is_windows = sys.platform == 'win32'

# Define the extension module within the 'polySim' package
c_module = Extension(
    'polySim.libpolySim',  # The module will be built as 'polySim/libpolySim.*'
    sources=['polySim/c_code/main.cpp'],
    include_dirs=[np.get_include()],
    language='c++',
    extra_compile_args=['/O2'] if is_windows else ['-O3'],
    extra_link_args=[],
)

setup(
    name='polySim',  # Unique name for your package on PyPI
    version='0.1.1',        # Follow semantic versioning
    description='Polycrystalline microstructure simulation package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Ensure PyPI renders it correctly
    author='Nikhil Chaurasia Sandeep Sangal, Shikhar Krishn Jha',
    author_email='nikolspace@gmail.com',
    url='https://github.com/nikolspace/polySim',  # URL to your package's repository
    packages=['polySim'],
    ext_modules=[c_module],
    install_requires=['numpy'],
    include_package_data=True,
    package_data={'polySim': ['*.pyd', '*.so', '*.dll']},
    zip_safe=False,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: C++',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',  
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
    ],
    python_requires='>=3.6',
)
