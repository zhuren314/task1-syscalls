PYTHON3 ?= python3
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

check:
	$(PYTHON3) ${ROOT_DIR}/test_wrapper.py
	$(PYTHON3) ${ROOT_DIR}/test_asm.py
