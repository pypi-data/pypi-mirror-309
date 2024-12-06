from setuptools import setup, find_packages

setup(
    name='puzan-hello-world-_my_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here, e.g., 'requests'
    ],
    description='A simple example Python package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
