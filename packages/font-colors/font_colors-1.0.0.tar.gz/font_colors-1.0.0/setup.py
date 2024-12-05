from setuptools import setup, find_packages

setup(
    name="font-colors",  # Name of your library
    version="1.0.0",  # Version of your library
    packages=find_packages(),
    install_requires=['colorama'],  # List any dependencies if needed
    description="none",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url="https://github.com/yourusername/mylibrary",  # URL of your GitHub repo
    author="Arsam",
    author_email="ashouriarsam@gmail.com",
    #license="MIT",  # Or any other license
)
