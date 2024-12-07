from setuptools import setup, find_packages

setup(
    name="OpenWhisper",
    version="0.1.0",
    description="A Whisper transcription client for seamless audio processing.",
    author="difansyah",
    author_email="dickyalfansyaah@gmail.com",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
