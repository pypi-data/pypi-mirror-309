from setuptools import setup, find_packages

setup(
    name='ibb_api_arsivi',
    version="0.1.0",
    description="Lorem ipsum dolor sit amet",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ceyda Özarslan",
    author_email="ceyzarslan@gmail.com",
    packages=find_packages(),
    install_requires=["pandas", "requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"

)
