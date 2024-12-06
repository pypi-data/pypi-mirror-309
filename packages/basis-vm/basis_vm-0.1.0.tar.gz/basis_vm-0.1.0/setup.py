from setuptools import setup, find_packages

setup(
    name='basis_vm',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "pymongo==4.1.1"
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here
        ],
    },
    author='BASE COMPUTING S.A.S.',
    author_email='social@basecomputing.com.co',
    description='A complete Python virtual machine for executing smart contracts.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/base-computing/basis_vm',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)