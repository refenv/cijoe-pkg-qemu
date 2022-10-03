---
doc: |
  This workflow demonstrates how to use qemu via cijoe in steps of:

  * Build qemu from source
  * Install qemu
  * Provision a guest using a cloudinit image
    - inject "$HOME/.ssh/id_rsa.pub" into guest as authorized_keys
  * Start the provisioned guest
  * Run a command within the provisioned guest
  * Stop the guest again

  This is done via worklets, which in turn are utilizing helper-functions from cijoe.qemu.wrapper.

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
  uses: qemu.guest_start_nvme
#  with:
#    nvme_img_root: "/tmp"

- name: check
  run: |
    hostname

- name: kill
  uses: qemu.guest_kill
