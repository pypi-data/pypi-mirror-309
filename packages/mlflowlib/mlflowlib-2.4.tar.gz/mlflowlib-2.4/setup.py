from setuptools import find_packages, setup

setup(
    name='mlflowlib',
    packages=find_packages(include=['mlflowlib']),
    version='2.4',
    license='MIT',    
    description='a general-purpose python package with MLflow integration',
    author='irem ozdemir',
    author_email = 'iremozdemirwww3@gmail.com', 
    keywords='mlflow',
    install_requires=[
        'mlflow>=1.21.0', 
        'tensorflow>=2.5.0',  
    ],
    url = 'https://github.com/iremozdemr/mlflowlib', 
    download_url = 'https://github.com/iremozdemr/mlflowlib/archive/refs/tags/2.4.tar.gz',
)