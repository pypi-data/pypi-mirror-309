from setuptools import setup, find_packages

setup(
    name='py-own-synonyms-pkg',  # Replace with your desired package name
    version='0.1.3',  # Version of your package
    packages=find_packages(),
    include_package_data=True,  # Ensure the JSON file is included
    install_requires=[],  # List dependencies here if needed
    long_description=open('README.md').read(),  # Optional, if you have a README
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Adjust for your minimum Python version
)
