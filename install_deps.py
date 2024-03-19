# Copyright (c) 2023-2024 Contributors to the Eclipse Foundation
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

import subprocess
import os
from argparse import ArgumentParser
from pathlib import Path

from velocitas_lib import get_workspace_dir


def safe_get_workspace_dir() -> str:
    """A safe version of get_workspace_dir which defaults to '.'."""
    try:
        return get_workspace_dir()
    except:
        return "."



def install_deps_via_conan(
    build_arch: str, is_debug: bool = False, build_all_deps: bool = False
) -> None:
    build_variant = "debug" if is_debug else "release"
    profile_filename = f"linux_{build_arch}_{build_variant}"
    profile_host_path = (
        Path(__file__)
        .absolute()
        .parent.joinpath(".conan", "profiles", profile_filename)
    )

    build_folder = os.path.join(safe_get_workspace_dir(), "build")
    os.makedirs(build_folder, exist_ok=True)

    deps_to_build = "missing" if not build_all_deps else "*"
    subprocess.check_call(
        [
            "conan",
            "install",
            "-pr:h",
            profile_host_path,
            "--build",
            deps_to_build,
            "..",
        ],
        cwd=build_folder,
    )


def cli() -> None:
    argument_parser = ArgumentParser(description="Installs dependencies")
    argument_parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Installs all dependencies in debug mode.",
    )
    argument_parser.add_argument(
        "-r",
        "--release",
        action="store_true",
        help="Installs all dependencies in release mode.",
    )
    argument_parser.add_argument(
        "-ba",
        "--build-all-deps",
        action="store_true",
        help="Forces all dependencies to be rebuild from source.",
    )
    args = argument_parser.parse_args()

    host_arch = subprocess.check_output(["arch"], encoding="utf-8").strip()

    install_deps_via_conan(
        host_arch, args.debug or not args.release, args.build_all_deps
    )


if __name__ == "__main__":
    cli()
