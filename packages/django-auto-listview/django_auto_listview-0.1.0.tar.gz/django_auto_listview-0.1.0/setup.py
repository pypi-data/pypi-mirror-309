from setuptools import setup, find_packages

setup(
    name="django-auto-listview",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django>=3.2"],
    description="A Django app for dynamic admin list views.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mohamad Bagher Davoodi",
    author_email="mohamadbagherdavoodi@gmail.com",
    url="https://github.com/smbd1368/django-auto-listview",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

