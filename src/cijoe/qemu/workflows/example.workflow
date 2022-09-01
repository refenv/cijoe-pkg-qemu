---
doc: |
  This workflow demonstrates how to use qemu via cijoe in steps of:

  * Build qemu from source
  * Instal qemu
  * Provision a guest using a cloudinit image
  * Start the provisioned guest
  * Run a command within the guest
  * Stop the guest again

  This is done via worklets, which in turn are utilizing helper-functions from joe.qemu.wrapper.

  When using a configuration with this workflow which looks in { local.env.HOME }, then this
  workflow does not require root/sudo.

steps:
- name: build
  uses: qemu.build_x86

- name: install
  uses: qemu.install

- name: cloudinit
  uses: qemu.guest_cloudinit

- name: start
  uses: qemu.guest_start

- name: check
  run: |
    hostname

- name: kill
  uses: qemu.guest_kill
