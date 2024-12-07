from setuptools import setup, find_packages

setup(
    name='grayhacker',
    version='0.1.0',
    description='A library for automating Selenium WebDriver setup',
    author='Your Name',
    author_email='your_email@example.com',
    packages=find_packages(),
    install_requires=[
        'selenium'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
