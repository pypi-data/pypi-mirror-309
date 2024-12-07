from setuptools import setup, find_packages

setup(
    name='AnyScrape',
    version='0.1.2',
    description="A one-liner Python library to scrape headlines, links, and images from any webpage.",
    long_description="Read README.md in the github for more details on how to use it",
    author='Diksha, Ayush Kumar Verma',
    author_email='diksha260303official@gmail.com , vermaayush5535@gmail.com',
    url='https://github.com/Diksha-Binary-Ninja/AnyScrape',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
