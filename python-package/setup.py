from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vnstock',
    version='0.1.0',
    description='A Python package for retrieving data from VNDIRECT API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nguyen Ngoc Binh',
    author_email='nguyenngocbinhneu@gmail.com',
    url='https://github.com/nguyenngocbinh/vnstock',
    packages=['vnstock'],
    install_requires=[
        'pandas',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
    ],
)
