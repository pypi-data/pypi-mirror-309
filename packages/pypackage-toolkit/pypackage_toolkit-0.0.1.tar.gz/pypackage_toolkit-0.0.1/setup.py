import setuptools

# from pkg_resources import parse_version
from configparser import ConfigParser


# note: all settings are in settings.ini; edit there, not here
config = ConfigParser(delimiters=["="])
config.read("settings.ini")
cfg = config["DEFAULT"]
requirements = cfg.get("requirements", "").split()

setuptools.setup(
    name="pypackage-toolkit",
    version="0.0.1",
    packages=setuptools.find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)
