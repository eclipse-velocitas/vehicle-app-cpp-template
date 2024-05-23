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

"""
Install all software depenencies of the given Velocitas project via a
simple command line interface.
"""

import os
import subprocess
from argparse import ArgumentParser
from pathlib import Path

from shared_utils import get_valid_arch
from velocitas_lib import get_workspace_dir


def safe_get_workspace_dir() -> str:
    """A safe version of get_workspace_dir which defaults to '.'."""
    try:
        return get_workspace_dir()
    except Exception:
        return "."


def get_profile_name(arch: str, build_variant: str) -> str:
    """Return the Conan profile name for the given `arch` and
    `build_variant`.

    Args:
        arch (str): The architecture of the profile.
        build_variant (str): The build variant (debug or release).

    Returns:
        str: The Conan profile name.
    """
    return f"linux_{get_valid_arch(arch)}_{build_variant}"


def install_deps_via_conan(
    build_arch: str,
    host_arch: str,
    is_debug: bool = False,
    build_all_deps: bool = False,
) -> None:
    build_variant = "debug" if is_debug else "release"

    profile_build_path = (
        Path(__file__)
        .absolute()
        .parent.joinpath(
            ".conan", "profiles", get_profile_name(build_arch, build_variant)
        )
    )

    profile_host_path = (
        Path(__file__)
        .absolute()
        .parent.joinpath(
            ".conan", "profiles", get_profile_name(host_arch, build_variant)
        )
    )

    build_folder = os.path.join(safe_get_workspace_dir(), "build")
    os.makedirs(build_folder, exist_ok=True)

    deps_to_build = "missing" if not build_all_deps else "*"

    toolchain = f"/usr/bin/{host_arch}-linux-gnu"
    build_host = f"{host_arch}-linux-gnu"
    cc_compiler = "gcc"
    cxx_compiler = "g++"

    os.environ["CONAN_CMAKE_FIND_ROOT_PATH"] = toolchain
    os.environ["CONAN_CMAKE_SYSROOT"] = toolchain
    os.environ["CC"] = f"{build_host}-{cc_compiler}"
    os.environ["CXX"] = f"{build_host}-{cxx_compiler}"

    subprocess.check_call(
        [
            "conan",
            "install",
            "-pr:h",
            profile_host_path,
            "-pr:b",
            profile_build_path,
            "--build",
            deps_to_build,
            "..",
        ],
        env=os.environ,
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
    argument_parser.add_argument(
        "-x",
        "--cross",
        action="store",
        help="Enables cross-compilation to the defined target architecture.",
    )
    args = argument_parser.parse_args()

    build_arch = subprocess.check_output(["arch"], encoding="utf-8").strip()
    host_arch = args.cross

    if host_arch is None:
        host_arch = build_arch

    subprocess.check_call(["conan", "config", "set", "general.revisions_enabled=1"])

    install_deps_via_conan(
        build_arch, host_arch, args.debug and not args.release, args.build_all_deps
    )


if __name__ == "__main__":
    cli()
