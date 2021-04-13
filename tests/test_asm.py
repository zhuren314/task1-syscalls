#!/usr/bin/env python3

import sys, os, tempfile

from testsupport import run, subtest, info, warn, ensure_library


def main() -> None:
    # Get test abspath
    lib = ensure_library("librw_2.so")
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

        # Check that librw_2.so provides read() and write() symbols
        with subtest("Check that read and write functions are available in librw_2.so"):
            with open(f"{tmpdir}/stdout", "w+") as stdout:
                run(["nm", '-D', '--defined-only', str(lib)],
                    stdout=stdout)
            ok = 0
            with open(f"{tmpdir}/stdout", "r") as stdout:
                for l in stdout.readlines():
                    if l.endswith(" T read\n"):
                        ok += 1
                    elif l.endswith(" T write\n"):
                        ok += 1
                if ok != 2:
                    warn(f"{str(lib)} is not providing read, write, or both!")
                    return

        # Check that librw_2.so does not use the syscall() function from the libc
        with subtest("Check that the syscall() function from libc is not used"):
            with open(f"{tmpdir}/stdout", "w+") as stdout:
                run(["nm", '-u', str(lib)],
                    stdout=stdout)
            with open(f"{tmpdir}/stdout", "r") as stdout:
                for l in stdout.readlines():
                    if " U syscall@" in l:
                        warn("syscall() function from the libc is used")
                        return

if __name__ == "__main__":
    main()
