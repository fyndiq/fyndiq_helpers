from setuptools import setup, find_packages

setup(
    name="fyndiq_helpers",
    version="0.1.2",
    description="Helpers for fyndiq services",
    url="https://github.com/fyndiq/fyndiq_helpers",
    author="Fyndiq AB",
    author_email="support@fyndiq.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'cerberus'
    ],
    zip_safe=False
)
