import io
import os
import sys
from shutil import rmtree

from setuptools import Command, setup
from pkg_resources import parse_requirements

# Package meta-data.
NAME = "python3-captchaai"
DESCRIPTION = "Python 3.6+ CaptchaAI library with AIO module."
URL = "https://github.com/AndreiDrang/python3-captchaai.git"
EMAIL = "python-captcha@pm.me"
AUTHOR = "AndreiDrang"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.2"
with open("requirements.txt", "rt") as requirements_txt:
    REQUIRED = [str(requirement) for requirement in parse_requirements(requirements_txt)]


here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "../README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel distribution…")
        os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        print("🤖 Uploaded ...")
        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    packages=["python3_captchaai"],
    install_requires=REQUIRED,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email=EMAIL,
    package_dir={"python3-captchaai": "python3_captchaai"},
    include_package_data=True,
    py_modules=["python3_captchaai"],
    url=URL,
    license="MIT",
    keywords="""
                captcha 
				2captcha
				recaptcha
				geetest
				hcaptcha
				capypuzzle
				tiktok
				rotatecaptcha
				funcaptcha
				keycaptcha
				python3
				recaptcha
				captcha
				security
				tiktok
				python-library
				captcha.ai
               """,
    python_requires=REQUIRES_PYTHON,
    zip_safe=False,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: AsyncIO",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    # Build - `python setup.py bdist_wheel`
    # Upload package: `python3 setup.py upload`
    cmdclass={"upload": UploadCommand},
)
print("🤖 Success install ...")
