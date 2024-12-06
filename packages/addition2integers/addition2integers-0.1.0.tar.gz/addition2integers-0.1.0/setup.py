from setuptools import setup, find_packages

setup(
    name='addition2integers',  # Unique package name
    version='0.1.0',    # Version number
    author='Talha',
    author_email='your.email@example.com',
    description='A utility package for math and string operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MuhammadTalha-crypto/sum',
    packages=find_packages(where="src"),  # Automatically find packages
    package_dir={'': 'src'},  # Root of your source code
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
