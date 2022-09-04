#!/usr/bin/env python3
"""
initialize guest using boot-image
=================================

Retargetable: False
-------------------
"""
from cijoe.qemu.wrapper import Guest


def worklet_entry(args, cijoe, step):
    """Provision a qemu-guest using a cloud-init image"""

    guest = Guest(cijoe, cijoe.config)

    return guest.init_using_bootimg()
