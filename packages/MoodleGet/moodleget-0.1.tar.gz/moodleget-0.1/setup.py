from setuptools import setup, find_packages

setup(
    name="MoodleGet",
    version="0.1",
    description="convenient way to get data through Moodle's API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="dynamy",
    url="https://github.com/dynamyy/MoodleAPI",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.32.3"
    ],
)