#!/usr/bin/env bash
#
# qemu reference environment
#
# In this environment the 'devbox' has the qemu-binaries:
#
# * qemu-system-x86_64
# * qemu-img
#
# Available in $PATH
#
# QEMU Guests are stored in $HOME/guests
#
# A QEMU Guest is defined with the name 'emujoe' and thus lives in $HOME/guests/emujoe
#

## cijoe QEMU-module, SSH hostname and port of the machine with qemu
export QEMU_HOST="localhost"
export QEMU_HOST_USER="${USER}"
export QEMU_HOST_PORT=22

## cijoe QEMU-module, location of binaries on QEMU_HOST, change this to point it to a different
# qemu-system binary which is not available in PATH eg. /opt/qemu/bin/qemu-system-x86_64
export QEMU_HOST_SYSTEM_BIN=qemu-system-x86_64
export QEMU_HOST_IMG_BIN=qemu-img

## cijoe QEMU-module, location of guests on qemu-host
# Files related to a qemu-guest, such as boot.img, cloud-init user-data/meta-data, pidfile, etc.
# are stored in a subdirectory named 'QEMU_GUEST_NAME' in 'QEMU_GUESTS
export QEMU_GUESTS=${HOME}/guests

## cijoe QEMU-module, definition of a guest and how to access it via SSH
#
export QEMU_GUEST_NAME=emujoe
export QEMU_GUEST_SSH_FWD_PORT=2222
export QEMU_GUEST_CONSOLE=sock
export QEMU_GUEST_MEM=6G
export QEMU_GUEST_SMP=4
export QEMU_GUEST_KERNEL=0

# cijoe SSH-module configuration, pointing to the qemu-guest
export SSH_HOST=localhost
export SSH_PORT=$QEMU_GUEST_SSH_FWD_PORT
export SSH_USER=root
export SSH_NO_CHECKS=1
