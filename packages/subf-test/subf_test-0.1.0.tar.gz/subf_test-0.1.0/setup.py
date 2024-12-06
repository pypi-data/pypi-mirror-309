from setuptools import setup, find_packages

setup(
    name="subf-test",
    version="0.1.0",
    author="Matin",
    author_email="matinarjmandimood@gmail.com",
    description="A short description of your library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-library",
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[],  # List dependencies, e.g., ['requests', 'numpy']
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
