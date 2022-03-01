#!/usr/bin/env bash
#
# qemu reference environment
#
# In this environment the 'devbox' has qemu installed in '/opt/qemu', the installation is used to
# instantate a qemu-guest which is used as the 'test-target'. The auxilary files for the guest are
# stored in '/opt/guests/emujoe'
#

#
# cijoe QEMU-module configuration
export QEMU_HOST="localhost"
export QEMU_HOST_USER="${USER}"
export QEMU_HOST_PORT=22
export QEMU_HOST_SYSTEM_BIN=/opt/qemu/bin/qemu-system-x86_64
export QEMU_HOST_IMG_BIN=qemu-img
export QEMU_GUESTS=/opt/guests
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
