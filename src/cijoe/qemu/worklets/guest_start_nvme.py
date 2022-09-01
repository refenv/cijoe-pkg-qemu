#!/usr/bin/env python3
"""
Start a qemu-guest with NVMe devices
====================================

Retargetable: false
-------------------
"""
import errno
import logging as log

from cijoe.qemu.wrapper import Guest


def worklet_entry(args, cijoe, step):
    """Start a qemu guest"""

    guest = Guest(cijoe, cijoe.config)

    # NVMe configuration arguments, a single controller with two namespaces
    lbads = 12
    drive_size = "8G"

    controller = {
        "id": "nvme0",
        "serial": "deadbeef",
        "bus": "pcie_downstream_port1",
        "mdts": 7,
    }

    drive1 = {
        "id": "nvme0n1",
        "file": str(guest.guest_path / "nvme0n1.img"),
        "format": "raw",
        "if": "none",
        "discard": "on",
        "detect-zeroes": "unmap",
    }
    drive2 = {
        "id": "nvme0n2",
        "file": str(guest.guest_path / "nvme0n2.img"),
        "format": "raw",
        "if": "none",
        "discard": "on",
        "detect-zeroes": "unmap",
    }
    drives = [drive1, drive2]

    ns1 = {
        "id": "nvme0n1",
        "drive": "nvme0n1",
        "bus": "nvme0",
        "nsid": 1,
    }
    ns2 = {
        "id": "nvme0n2",
        "drive": "nvme0n2",
        "bus": "nvme0",
        "nsid": 2,
        "zoned": "on",
        "zoned.zone_size": 8192 << lbads,
        "zoned.zone_capacity": 4096 << lbads,
        "zoned.max_active": 256,
        "zoned.max_open": 256,
    }

    # Check that the backing-storage exists, create them if they do not
    for drive in drives:
        err, _ = cijoe.run_local(f"[ -f { drive['file'] } ]")
        if err:
            guest.image_create(drive["file"], drive["format"], drive_size)
        err, _ = cijoe.run_local(f"[ -f { drive['file'] } ]")

    # pcie setup
    nvme = []
    nvme += ["-device pcie-root-port,id=pcie_root_port1,chassis=1,slot=1"]
    nvme += ["-device x3130-upstream,id=pcie_upstream_port1,bus=pcie_root_port1"]
    nvme += [
        "-device xio3130-downstream"
        ",id=pcie_downstream_port1,bus=pcie_upstream_port1,chassis=2,slot=1"
    ]

    nvme += [
        "-device nvme," + ",".join([f"{k}={v}" for k, v in controller.items()]),
        "-drive " + ",".join([f"{k}={v}" for k, v in drive1.items()]),
        "-device nvme-ns," + ",".join([f"{k}={v}" for k, v in ns1.items()]),
        "-drive " + ",".join([f"{k}={v}" for k, v in drive2.items()]),
        "-device nvme-ns," + ",".join([f"{k}={v}" for k, v in ns2.items()]),
    ]

    err = guest.start(extra_args=nvme)
    if err:
        log.error(f"guest.start() : err({err})")
        return err

    started = guest.is_up()
    if not started:
        log.error("guest.is_up() : False")
        return errno.EAGAIN

    return 0
