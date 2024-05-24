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

import json
import os
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from typing import List

from shared_utils import get_valid_arch
from velocitas_lib import get_workspace_dir

CMAKE_EXECUTABLE = "cmake"
CONAN_EXECUTABLE = "conan"


def safe_get_workspace_dir() -> str:
    """A safe version of get_workspace_dir which defaults to '.'."""
    try:
        return get_workspace_dir()
    except Exception:
        return "."


def get_build_tools_path(build_folder_path: str) -> str:
    paths: List[str] = []
    with open(
        os.path.join(build_folder_path, "conanbuildinfo.txt"), encoding="utf-8"
    ) as file:
        for line in file:
            if line.startswith("PATH="):
                path_list = json.loads(line[len("PATH=") :])
                paths.extend(path_list)
    return ";".join(paths)


def print_build_info(
    build_variant: str,
    build_arch: str,
    host_arch: str,
    build_target: str,
    is_static_build: bool,
) -> None:
    """Print information about the build.

    Args:
        build_variant (str): The variant of the build: "release" or "debug"
        build_arch (str): The architecture the app is built for.
        build_target (str): Which artefact is being built.
        is_static_build (bool): Enable static building.
    """
    cmake_version = subprocess.check_output(
        [CMAKE_EXECUTABLE, "--version"], encoding="utf-8"
    ).strip()
    conan_version = subprocess.check_output(
        [CONAN_EXECUTABLE, "--version"], encoding="utf-8"
    ).strip()

    print(f"CMake version      {cmake_version}")
    print(f"Conan version      {conan_version}")
    print(f"Build arch         {build_arch}")
    print(f"Host arch          {host_arch}")
    print(f"Build variant      {build_variant}")
    print(f"Build target       {build_target}")
    print(f"Static build       {'yes' if is_static_build else 'no'}")


def build(
    build_variant: str,
    build_arch: str,
    host_arch: str,
    build_target: str,
    static_build: bool,
    coverage: bool = True,
) -> None:
    build_folder = os.path.join(safe_get_workspace_dir(), "build")

    cxx_flags = ["-g"]
    if coverage:
        cxx_flags.append("--coverage")

    if build_variant == "release":
        cxx_flags.append("-O3")
    else:
        cxx_flags.append("-O0")

    os.makedirs(build_folder, exist_ok=True)

    xcompile_toolchain_file = ""
    if build_arch != host_arch:
        profile_build_path = (
            Path(__file__)
            .absolute()
            .parent.joinpath("cmake", f"{build_arch}_to_{host_arch}.cmake")
        )
        xcompile_toolchain_file = f"-DCMAKE_TOOLCHAIN_FILE={profile_build_path}"

    subprocess.run(
        [
            CMAKE_EXECUTABLE,
            "--no-warn-unused-cli",
            "-DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE",
            f"-DCMAKE_BUILD_TYPE:STRING={build_variant}",
            f'-DBUILD_TOOLS_PATH:STRING="{get_build_tools_path(build_folder)}"',
            f"-DSTATIC_BUILD:BOOL={'TRUE' if static_build else 'FALSE'}",
            xcompile_toolchain_file,
            "-S..",
            "-B.",
            "-G",
            "Ninja",
            f"-DCMAKE_CXX_FLAGS={' '.join(cxx_flags)}",
        ],
        cwd=build_folder,
    )
    subprocess.run(
        [
            CMAKE_EXECUTABLE,
            "--build",
            ".",
            "--config",
            build_variant,
            "--target",
            build_target,
        ],
        cwd=build_folder,
    )


def cli() -> None:
    parser = ArgumentParser(
        description="""Build targets of the project
============================================================================
Builds the targets of the project in different flavors."""
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        const="debug",
        dest="variant",
        help="Builds the target(s) in debug mode.",
    )
    parser.add_argument(
        "-r",
        "--release",
        action="store_const",
        const="release",
        dest="variant",
        help="Builds the target(s) in release mode.",
    )
    parser.add_argument(
        "-t", "--target", help="Builds only the target <name> instead of all targets."
    )
    parser.add_argument(
        "-s", "--static", action="store_true", help="Links all dependencies statically."
    )
    parser.add_argument(
        "-x",
        "--cross",
        action="store",
        help="Enables cross-compilation to the defined target architecture.",
    )
    args = parser.parse_args()
    if not args.variant:
        args.variant = "debug"
    if not args.target:
        args.target = "all"
    build_arch = subprocess.check_output(["arch"], encoding="utf-8").strip()

    host_arch = args.cross

    if host_arch is None:
        host_arch = build_arch
    else:
        host_arch = get_valid_arch(host_arch)

    print_build_info(args.variant, build_arch, host_arch, args.target, args.static)
    build(args.variant, build_arch, host_arch, args.target, args.static)


if __name__ == "__main__":
    cli()
