from setuptools import setup, find_packages

setup(
    name='AnyScrape',
    version='0.1.0',
    description='A simple one-liner web scraper for basic tasks.',
    authors='Diksha, Ayush',
    authors_email='diksha260303official@gmail.com , vermaayush5535@gmail.com',
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
