#!/usr/bin/env python3

import sys, os, tempfile

from testsupport import run, subtest, info, warn, ensure_library


def main() -> None:
    # Get test abspath
    lib = ensure_library("librw-2.so")
    with tempfile.TemporaryDirectory() as tmpdir:

        # Generate a small random file
        with open(f"{tmpdir}/rdn.txt", "wb") as fp:
            fp.write(os.urandom(4096))

        # Copy the file with the system's glibc
        with subtest("Run cp with system glibc"):
            run(["cp", f"{tmpdir}/rdn.txt", f"{tmpdir}/rdn.glibc.txt"])

        # Copy files with LD_PRELOADed librw.so.2
        with subtest(f"Run cp with {lib} preloaded"):
            with open(f"{tmpdir}/stderr", "w+") as stderr:
                run(
                    ["cp", f"{tmpdir}/rdn.txt", f"{tmpdir}/rdn.librw.2.txt"],
                    extra_env={"LD_PRELOAD": str(lib)},
                    stderr=stderr,
                )
            with open(f"{tmpdir}/stderr", "r") as stderr:
                for l in stderr.readlines():
                    if "ERROR: ld.so:" in l:
                        warn(l)
                        return

        # Check that glibc and librw.so.2 give the same result
        with subtest("Check that both resulting files are identical"):
            run(["cmp", f"{tmpdir}/rdn.glibc.txt", f"{tmpdir}/rdn.librw.2.txt"])


if __name__ == "__main__":
    main()
