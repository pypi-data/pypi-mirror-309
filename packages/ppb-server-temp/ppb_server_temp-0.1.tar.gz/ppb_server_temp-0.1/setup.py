from setuptools import setup, find_packages

setup(
    name='ppb-server-temp',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'pytest',
        'pytest-cov',
        'pymongo',
    ],
    author='Michael',
    description='A package for my server',
    url='https://github.com/FloresTristan/ppb-server-temp',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
