from setuptools import setup

setup(
    name="powerline-tailscale",
    description="A Powerline segment for showing the status of Tailscale",
    readme="README.md",
    version="1.0.1",
    keywords="powerline tailscale",
    license="MIT",
    author="Üllar Seerme",
    url="https://github.com/usrme/powerline-tailscale",
    packages=["powerline_tailscale"],
    python_requires=">=3.9",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Terminals",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
