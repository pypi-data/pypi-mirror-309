from setuptools import setup, find_packages

setup(
    name='lilliepy',  
    version='0.8.0',  
    packages=find_packages(),  
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={
        'lilliepy': ['bin.bat', 'bin.sh']
    },
    include_package_data=True,
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown"
)
