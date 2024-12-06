from setuptools import setup, find_packages

setup(
    name="shakshippm_31",  # The name of your package
    version="0.1.2",  # Version of your package
    author="shakshi",  # Your name
    author_email="shakshibisht7@gmail.com",  # Your email
    description="A package manager that installs adaboost, sklearn, dataframe, and pandas",
    long_description=open("README.md").read(),  # Content from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sppm",  # Optional: GitHub link
    packages=find_packages(),  # Automatically finds sub-packages
    install_requires=[
        "scikit-learn",  # Includes AdaBoost
        "pandas",        # For DataFrames
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version
)
