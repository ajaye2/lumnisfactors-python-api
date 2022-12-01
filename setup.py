import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lumnisfactors",
    packages = ['lumnisfactors'],
    version="0.3",
    author="Abubakarr Jaye",
    author_email="ajaye@lumnis.org",
    description="Lumnis Alternative Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lumnisfactors/lumnisfactors-python-api/archive/refs/tags/v0.3.tar.gz",
    py_modules = ["lumnis"],
    install_requires=[
        'grequests',
        'pandas',
        'requests',
        'numpy'
],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)