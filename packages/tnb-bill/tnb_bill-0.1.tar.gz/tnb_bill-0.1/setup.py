from setuptools import setup, find_packages

setup(
    name='tnb_bill',  # Name of your package
    version='0.1',
    packages=find_packages(),
    description='A package to calculate electricity bills by TNB',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='zhamri',
    author_email='zhamri@gmail.com',
    url='https://github.com/zhamri/tnb_bill',  # Replace with your GitHub repo URL
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
