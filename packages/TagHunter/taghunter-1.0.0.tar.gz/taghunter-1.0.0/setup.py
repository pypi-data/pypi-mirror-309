from setuptools import setup, find_packages

setup(
    name='TagHunter',
    version='1.0.0',
    description='A Python package to identify and analyze improperly structured <p> tags in HTML documents.',
    long_description='''
        TagHunter is a Python tool for identifying <p> tags in HTML files that are not properly nested, such as <p> tags that appear as list items but are not part of <li> tags. 

        Features:
        - Detect improperly structured <p> tags.
        - Recognize patterns like numeric, Roman numerals, and parenthetical markers.
        - Validate patterns and classify by CSS classes.
        - Exclude invalid patterns (e.g., numbers above a threshold).
        - Aggregate results and generate reports.
        - Automatically export findings to CSV files.
    ''',
    long_description_content_type='text/plain',
    author='Birbal Kumar',
    author_email='birbalk99@gmail.com',
    url='https://github.com/Birbalk99/TagHunter',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
        'beautifulsoup4>=4.9.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
