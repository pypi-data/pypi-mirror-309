from setuptools import setup, find_packages
import requests
urls = "https://github.com/Diksha-Binary-Ninja/AnyScrape/blob/main/README.md"
response = requests.get(urls)
long_description = response.text if response.status_code == 200 else "A simple scraping library."
setup(
    name='AnyScrape',
    version='0.1.1',
    description="A one-liner Python library to scrape headlines, links, and images from any webpage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
