from setuptools import setup, find_packages

setup(
    name='disgrasya',
    version='5.30.0',
    description='A utility for checking credit cards through multiple gateways using multi-threading and proxies.',
    author='Jaehwan0',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'disgrasya=disgrasya.main:main',
        ],
    },
)
