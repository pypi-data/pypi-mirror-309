from setuptools import setup, find_packages

setup(
    name="RediCMS",
    version="0.2.0",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/redicms",
    author="Anvish Inc.",
    author_email="anvish@anvish.in",
    license="CC-BY-NC-ND-4.0",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "django>=5.1.3",
        "djangorestframework>=3.15.2"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Programming Language :: Python :: 3.12",
        "License :: Other/Proprietary License",
    ],
    python_requires=">=3.12",
)
