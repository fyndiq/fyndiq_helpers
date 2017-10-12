from setuptools import setup, find_packages

setup(
    name="global_platform_helpers",
    version="0.1.0",
    description="Helpers for fyndiq services",
    url="https://github.com/fyndiq/global_platform_helpers",
    author="Fyndiq AB",
    author_email="support@fyndiq.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'cerberus'
    ],
    zip_safe=False
)
