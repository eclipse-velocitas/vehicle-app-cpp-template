# Copyright (c) 2024 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

import os.path
import re
import subprocess
import time
from typing import List, NamedTuple

DOWNLOAD_DIR = "./apt_packages"

installed_apt_packages = subprocess.check_output(["apt", "list", "--installed"], encoding="utf-8")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

subprocess.check_call(["sudo", "cp", "/etc/apt/sources.list", "/etc/apt/sources.list~"])
subprocess.check_call(["sudo", "sed", "-Ei", "s/^# deb-src /deb-src /", "/etc/apt/sources.list"])
subprocess.check_call(["sudo", "apt-get", "update"])

max_retries = 3
retry_delay = 5

PACKAGE_INFO_PATTERN = re.compile(r"([\w+-\.]+)\/([\w-]+,)*now\s([\w\.+-_~]+)\s(\w+)\s\[(.+)\]")

class PackageInfo(NamedTuple):
    name: str
    repos: str
    version: str

def extract_package_info(package_info: str) -> PackageInfo:
    print(package_info)
    match = PACKAGE_INFO_PATTERN.match(package_info)

    return PackageInfo(match.group(1), match.group(2), match.group(3))


def clean_archives():
    for file in os.listdir(DOWNLOAD_DIR):
        path = os.path.join(DOWNLOAD_DIR, file)
        if not os.path.isdir(path):
            os.unlink(path)

def download_package_sources(package_info: PackageInfo):
    retries = 0
    while retries < max_retries:
        try:
            subprocess.check_call(["apt", "source", f"{package_info.name}={package_info.version}"], cwd=DOWNLOAD_DIR)
            clean_archives()
            print(f"Successfully processed package: {package_info.name}")

            break
        except subprocess.CalledProcessError as e:
            retries += 1
            print(f"Failed to process package {package_info.name}, retry {retries}/{max_retries}: {e}")
            package_info = PackageInfo(package_info.name, package_info.repos, package_info.version.split('-')[0])
            if retries < max_retries:
                time.sleep(retry_delay)
            else:
                if "GITHUB_STEP_SUMMARY" in os.environ:
                    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
                        print(f"Failed to process package {package_info.name}={package_info.version}", file=f)


def process_installed_packages(package_infos: List[str]):
    for package in package_infos:
        if len(package.strip()) == 0:
            continue

        package_info = extract_package_info(package)
        print(f"Processing package: {package_info.name}, version: {package_info.version}")
        download_package_sources(package_info)



if __name__ == "__main__":
    process_installed_packages(installed_apt_packages.split("\n")[2:])
