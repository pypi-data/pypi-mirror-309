# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 JinTian.
#
# This file is part of alfred
# (see http://jinfagang.github.io).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
"""
install alfred into local bin dir.
"""
import subprocess
from setuptools import find_namespace_packages, setup, find_packages
from setuptools import setup, Extension
import io
from os import path
from setuptools.command.install import install

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


version_file = "maskgct/version.py"


def get_version():
    with open(version_file, "r") as f:
        exec(compile(f.read(), version_file, "exec"))
    return locals()["__version__"]


class CustomInstallCommand(install):
    def run(self):
        subprocess.check_call(["pip", "install", "--no-deps", "py3langid"])
        subprocess.check_call(["pip", "install", "--no-deps", "LangSegment>=0.3.5"])
        install.run(self)


setup(
    name="maskgct",
    version=get_version(),
    keywords=["deep learning", "script helper", "tools"],
    description="MaskGCT convenient inference wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPL-3.0",
    classifiers=[
        # Operation system
        "Operating System :: OS Independent",
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Topics
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        # Pick your license as you wish
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # packages=find_packages(),
    # packages=['maskgct'],
    # packages=find_packages(include=['maskgct*']),  # 这会找到所有maskgct开头的包
    # packages=["maskgct", "maskgct.maskgct"],  # package_data={
    # #     "maskgct": ["tts/maskgct/config/*.json"],
    # # },
    packages=find_namespace_packages(include=["maskgct.*"]),
    include_package_data=True,
    entry_points={"console_scripts": ["maskgct-server = maskgct.maskgct.server:main"]},
    author="Lucas Jin",
    author_email="jinfagang19@163.com",
    url="https://github.com/lucasjinreal/MaskGCT",
    platforms="any",
    install_requires=[
        "pykakasi",
        "pyopenjtalk",
        "phonemizer",
        "cn2an",
        "pypinyin",
        "unidecode",
        "jieba",
        "json5"
    ],
    cmdclass={
        "install": CustomInstallCommand,
    },
)
