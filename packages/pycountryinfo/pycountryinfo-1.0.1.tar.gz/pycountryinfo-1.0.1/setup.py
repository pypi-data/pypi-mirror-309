from setuptools import setup, find_packages

setup(
    name='pycountryinfo',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Justice Nyame',
    author_email='nyamejustice2000@gmail.com',
    description='A Python package that provides information about countries, including their name, nationality, and other relevant data. Perfect for geographic data applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    url='https://github.com/Jnyame21/pycountryinfo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

