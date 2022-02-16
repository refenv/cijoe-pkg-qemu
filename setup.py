"""
    Definition of CIJOE/qemu distribution package
"""
import codecs
import glob
import os
from setuptools import setup


def scan_dfiles(path):
    """Scan for everything in path"""

    dfiles = {}
    for root, _, fnames in os.walk(path):
        install_path = os.path.join("share", "cijoe", root)
        if install_path not in dfiles:
            dfiles[install_path] = []

        for fname in fnames:
            dfiles[install_path].append(os.path.join(root, fname))

    listing = []
    for ipath, files in dfiles.items():
        listing.append((ipath, files))

    return listing


def read(*parts):
    """Read parts to use a e.g. long_description"""

    here = os.path.abspath(os.path.dirname(__file__))

    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as pfp:
        return pfp.read()


setup(
    name="cijoe-pkg-qemu",
    version="6.0.6",
    description="CIJOE: qemu package",
    long_description=read('README.rst'),
    author="Simon A. F. Lund",
    author_email="os@safl.dk",
    url="https://github.com/refenv/cijoe-pkg-qemu",
    license="Apache License 2.0",
    install_requires=[
        "cijoe (>=0.2.3)"
    ],
    zip_safe=False,
    data_files=[
        ("bin", glob.glob("bin/*")),

        ("share/cijoe/hooks", glob.glob("hooks/*")),
        ("share/cijoe/modules", glob.glob("modules/*.sh")),
        ("share/cijoe/envs", glob.glob("envs/*")),

    ] + scan_dfiles('testfiles') + [
        ("share/cijoe/testcases", glob.glob("testcases/*")),
        ("share/cijoe/testsuites", glob.glob("testsuites/*")),
        ("share/cijoe/testplans", glob.glob("testplans/*"))
    ],
    options={'bdist_wheel': {'universal': True}},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing"
    ],
)
