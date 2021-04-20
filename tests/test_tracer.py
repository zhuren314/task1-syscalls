#!/usr/bin/env python3

import sys, os, tempfile

from testsupport import run, subtest, info, warn, test_root, run_project_executable

def main() -> None:

    with tempfile.TemporaryDirectory() as tmpdir:

        # Generate a small random file
        with open(f"{tmpdir}/rdn.txt", "wb") as fp:
            fp.write(os.urandom(4096))

        # Run the test program
        with subtest("Checking read and write tracing"):
            with open(f"{tmpdir}/stderr", "w+") as stderr, open(f"{tmpdir}/stdout", "w+") as stdout:
                run_project_executable("tracer",
                                       args=[f"{test_root()}/test_tracer", f"{tmpdir}/rdn.txt"],
                                       stderr=stderr, stdout=stdout)
            with open(f"{tmpdir}/diffout", "w+") as diffout:
                run(["diff", f"{tmpdir}/stderr", f"{tmpdir}/stdout"],
                    stdout=diffout, check=False)
            with open(f"{tmpdir}/diffout", "r") as diffout:
                for l in diffout.readlines():
                    if l.startswith('>'):
                        warn("Your tracer missed calls to read or write or did not format the output correctly")
                        exit(1)

if __name__ == "__main__":
    main()
