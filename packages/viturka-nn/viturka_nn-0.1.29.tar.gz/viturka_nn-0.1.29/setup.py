from setuptools import setup, find_packages

setup(
    name='viturka_nn',
    version='0.1.29',
    description='A client library for deep federated learning platform.',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'torch',
        'torchvision',
        'torchmetrics>=0.11.0',
        'pycocotools',
        'scikit-learn'
    ],
    python_requires='>=3.6'
)