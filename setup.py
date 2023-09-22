from setuptools import setup

setup(
    name="powerline-tailscale",
    description="A Powerline segment for showing the status of Tailscale",
    version="1.0.0",
    keywords="powerline tailscale",
    license="MIT",
    author="Üllar Seerme",
    url="https://github.com/usrme/powerline-tailscale",
    packages=["powerline_tailscale"],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Terminals",
    ],
)
