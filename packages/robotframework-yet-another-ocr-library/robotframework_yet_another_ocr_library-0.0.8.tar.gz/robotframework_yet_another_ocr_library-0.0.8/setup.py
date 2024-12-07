from setuptools import setup, find_packages, Distribution


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    # pylint: disable=no-self-use
    def has_ext_modules(self):
        """Distribution which always forces a binary package with platform name"""
        return True


with open("src/RobotframeworkYetAnotherOcrLibrary/version.py", "r") as fh:
    VersionFile = fh.read()
    VersionFile = VersionFile.replace("\n", "")
    IGNORE, VERSION = VersionFile.split(" = ")
    VERSION = VERSION.replace("\"", "")

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = list(filter(lambda s: s != "", f.read().split("\n")))

setup(name="robotframework-yet-another-ocr-library",
      version=VERSION,
      description="Object recognition library for Robot Framework",
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      author="Andreas Sekulski",
      author_email="andreas.sekulski@gmail.com",
      url='https://github.com/Nepitwin/robotframework-yet-another-ocr-lib',
      license='APACHE',
      install_requires=REQUIREMENTS,
      packages=find_packages("src"),
      package_dir={"RobotframeworkYetAnotherOcrLibrary": "src/RobotframeworkYetAnotherOcrLibrary"},
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "License :: OSI Approved :: Apache Software License",
          "Topic :: Software Development :: Testing",
          "Framework :: Robot Framework",
          "Framework :: Robot Framework :: Library"
      ],
      distclass=BinaryDistribution,
      platforms=['Windows', 'Linux']
      )
