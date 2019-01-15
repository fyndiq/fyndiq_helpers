from setuptools import find_packages, setup

setup(
    name="fyndiq_helpers",
    version="0.2.1",
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
