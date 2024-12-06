from setuptools import setup, find_packages

setup(
    name="flask_api_package",
    version="1.0.0",
    description="A simple Flask API package",
    author="Your Name",
    author_email="your_email@example.com",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "flask-api=flask_api_package.app:create_app",
        ]
    },
)