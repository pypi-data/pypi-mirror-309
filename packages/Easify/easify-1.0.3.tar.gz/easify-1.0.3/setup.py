from setuptools import setup, find_packages

setup(
    name="Easify",  # Replace with your package name
    version="1.0.3",
    description="Prints preprocessing code for data engineering tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Taksh Dhabalia",
    author_email="no@example.com",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "print_preprocessing=Easify.main:print_preprocessing_code",
            "print1=Easify.main:print_1",
            "print2=Easify.main:print_2" ,
            "print_ap=Easify.main:print_ap",
             "print_dt=Easify.main:print_dt",
             "print_km=Easify.main:print_km", # Adjusted for Easify
        ],
    },

    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "scipy"
    ],
    python_requires=">=3.6",
)
