#!/usr/bin/env python3
"""
initialize guest os using cloud-init
====================================

Retargetable: False
-------------------
"""
from cijoe.qemu.wrapper import Guest


def worklet_entry(args, cijoe, step):
    """Provision a qemu-guest using a cloud-init image"""

    guest = Guest(cijoe, cijoe.config)

    return guest.cloudinit()
