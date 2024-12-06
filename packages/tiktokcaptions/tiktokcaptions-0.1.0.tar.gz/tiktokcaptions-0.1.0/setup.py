from setuptools import setup, find_packages

setup(
    name="tiktokcaptions",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "moviepy",
        "numpy",
        "Pillow",
        "opencv-python",
    ],
    package_data={
        'tiktokcaptions': ['assets/fonts/*.ttf'],
    },
    author="0xIbra",
    author_email="ibragim.ai95@gmail.com",
    description="Add TikTok-style captions to videos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/0xIbra/tiktokcaptions",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)