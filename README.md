# Task 1 - Kernel and System Calls

## Task 1.1

Write a wrapper for the `read` and `write` system calls by using the `syscall` function from the glibc. Add the following optimsation: if the number of bytes to read/write is 0, do not call the system call.

The resulting binary should be a shared library named `librw_1.so` and should be usable by any application to replace the original glibc implementations of these two wrappers without changing the behaviour of applications.

## Task 1.2

Reuse your wrappers from task 1.1 and replace the `syscall` function with assembly that performs the system call. You must manage error reporting in the same way the glibc would.

The resulting binary should be a shared library named `librw_2.so` and should be usable by any application to replace the original glibc implementations of these two wrappers without changing the behaviour of applications.

### Inline assembly
*For C/C++ users:* You can use `asm()` ([docs](https://gcc.gnu.org/onlinedocs/gcc/Using-Assembly-Language-with-C.html)).

*For Rust users:* You can use `asm!()` from rust nightly ([docs](https://doc.rust-lang.org/nightly/unstable-book/library-features/asm.html)).

## Task 1.3

I wanted to do something more complicated: implement an strace tool fully in userspace, without using kernel facilities. But that seems really hard/impossible (I thought they could LD_PRELOAD and replace the glibc `syscall` function, but that doesn't seem possible since `syscall` is a variadic function...

## Going further (not graded)

If you want to go further, you can try to implement a new system call in the Linux kernel. You can find a lot of documentation on the internet, as well as examples in the Linux kernel source code (you can use this [indexing website](https://elixir.bootlin.com/linux/latest/source) to easily navigate in kernel code).

## General information

1. Edit Makefile to include the build command used for your language
2. For building run 
   ```console
   $ make all
   ```
3. For running the tests run:
   ```console
   $ make check
   ```
