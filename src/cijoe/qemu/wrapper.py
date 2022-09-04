"""
    Wraps qemu binaries: system, qemu-img and provides "guest-control"

    NOTE: this wrapper is "local-only". That is, changing transport does not retarget
    the functionality provided here. Most of the code is utilizing Python modules such
    as shutil, pathlib, psutil, download/requests. To make this re-targetable these
    things must be done via command-line utilities. It is certainly doable, however,
    currently not a priority as the intent is to utilize qemu to produce a virtual
    machine to serve as a 'target' for tests.
"""
import logging as log
import os
import shutil
import time
from pathlib import Path

import psutil
from cijoe.core.misc import download


def qemu_img(cijoe, args=""):
    """Helper function wrapping around 'qemu-img'"""

    return cijoe.run_local(f"{cijoe.config.options['qemu']['img_bin']} {args}")


def qemu_system(cijoe, args=""):
    """Wrapping the qemu system binary"""

    return cijoe.run_local(f"{cijoe.config.options['qemu']['system_bin']} {args}")


class Guest(object):
    def __init__(self, cijoe, config, name=None):
        """."""

        self.cijoe = cijoe

        self.qemu_config = config.options.get("qemu", None)
        if not name:
            name = sorted(self.qemu_config["guests"].keys())[0]

        self.guest_config = self.qemu_config["guests"][name]

        self.guest_path = (Path(self.guest_config["path"])).resolve()
        self.boot_img = self.guest_path / "boot.img"
        self.seed_img = self.guest_path / "seed.img"
        self.pid = self.guest_path / "guest.pid"
        self.monitor = self.guest_path / "monitor.sock"
        self.serial = self.guest_path / "serial.output"

    def image_create(self, filename, fmt="raw", size="8GB"):
        """
        Creates an image-file in the guest_path. Returns 0 on succes, errno to
        indicate the error.
        """

        img_path = self.guest_path / filename
        err, _ = qemu_img(self.cijoe, f"create -f {fmt} {img_path} {size}")

        return err

    def is_initialized(self):
        """Check that the guest is initialized"""

        return self.guest_path.exists()

    def is_running(self):
        """Check whether the guest is running"""

        pid = self.get_pid()

        return pid and psutil.pid_exists(pid)

    def get_pid(self):
        """Returns pid from 'guest.pid', returns 0 when 'guest.pid' is not found"""

        if not self.pid.exists():
            return 0

        with self.pid.open() as pidfile:
            pid = int(pidfile.read().strip())

        return pid

    def initialize(self):
        """Create a 'home' for the guest'"""

        os.makedirs(self.guest_path, exist_ok=True)

    def is_up(self, timeout=120):
        """Wait at most 'timeout' seconds for the guest to print 'login' to serial"""

        if not self.is_running():
            return False

        began = time.time()
        while True:
            enter = time.time()
            try:
                with self.serial.open() as serialfile:
                    if "login:" in serialfile.read():
                        return True
            except Exception as exc:
                log.error(f"{exc}")

            now = time.time()
            elapsed_iter = now - enter
            elapsed_total = now - began

            if elapsed_iter < 5.0:
                time.sleep(5.0 - elapsed_iter)
            if elapsed_total > timeout:
                return False

    def start(self, daemonize=True, extra_args=[]):
        """."""

        args = []

        # Create qemu-system args
        for key, value in self.guest_config["system_args"].items():
            args.append(f"-{key}")
            if isinstance(value, dict):
                args.append(next((f"{opt}={val}" for opt, val in value.items())))
            else:
                args.append(str(value))

        # magic-option, when 'boot.img' exists, add it is as boot-drive
        if self.boot_img.exists():
            args += [
                "-blockdev",
                f"qcow2,node-name=boot,file.driver=file,file.filename={self.boot_img}",
            ]
            args += ["-device", "virtio-blk-pci,drive=boot"]

        #
        # Fancy-args
        #
        host_share = self.guest_config["fancy"].get("host_share", None)
        if host_share:
            host_share = Path(host_share).resolve()
            args += [
                "-virtfs",
                "fsdriver=local,id=fsdev0,security_model=mapped,mount_tag=hostshare"
                f",path={host_share}",
            ]

        ports = self.guest_config["fancy"].get("tcp_forward", None)
        if ports:
            args += [
                "-netdev",
                f"user,id=n1,ipv6=off,hostfwd=tcp::{ports['host']}-:{ports['guest']}",
            ]
            args += ["-device", "virtio-net-pci,netdev=n1"]

        # Management stuff
        args += ["-pidfile", str(self.pid)]
        args += ["-monitor", f"unix:{self.monitor},server,nowait"]

        if daemonize:
            args += ["-display", "none"]
            args += ["-serial", f"file:{self.serial}"]
            args += ["-daemonize"]
        else:
            args += ["-nographic"]
            args += ["-serial", "mon:stdio"]

        args += extra_args

        args += [self.guest_config.get("extra_args", "")]

        err, _ = qemu_system(self.cijoe, " ".join(args))

        return err

    def kill(self):
        """Shutdown qemu guests by killing the process using the 'guest.pid'"""

        err = 0

        pid = self.get_pid()
        if pid:
            qemu_proc = psutil.Process(pid)
            qemu_proc.terminate()

            gone, alive = psutil.wait_procs([qemu_proc], timeout=3)
            for proc in alive:
                proc.kill()

        return err

    def init_using_cloudimg(self):
        """Provision a guest OS using cloudinit"""

        # Ensure the guest is *not* running
        self.kill()

        # Ensure the guest has a "home"
        self.initialize()

        # Ensure the guest has a cloudinit-image available for "installation"
        cloudinit = self.cijoe.config.options["cloudinit"].get(
            self.guest_config["cloudinit"]
        )
        cloudinit["img"] = Path(cloudinit["img"]).resolve()

        if not cloudinit["img"].exists():
            os.makedirs(cloudinit["img"].parent, exist_ok=True)
            err, path = download(cloudinit["url"], cloudinit["img"])
            if err:
                log.error(f"download({cloudinit['url']}), {path}: failed")
                return err

        # Create the boot.img based on cloudinit_img
        shutil.copyfile(str(cloudinit["img"]), str(self.boot_img))
        qemu_img(self.cijoe, f"resize {self.boot_img} 10G")

        # Create seed.img, with data and meta embedded
        metadata_path = shutil.copyfile(
            cloudinit["meta"], self.guest_path / "meta-data"
        )
        userdata_path = shutil.copyfile(
            cloudinit["user"], self.guest_path / "user-data"
        )
        with Path(cloudinit["pubkey"]).resolve().open() as kfile:
            pubkey = kfile.read()
        with userdata_path.open("a") as userdatafile:
            userdatafile.write("ssh_authorized_keys:\n")
            userdatafile.write(f"- {pubkey}\n")

        cloud_cmd = " ".join(
            [
                "cloud-localds",
                "-v",
                str(self.seed_img),
                str(userdata_path),
                str(metadata_path),
            ]
        )
        err, _ = self.cijoe.run_local(cloud_cmd)

        # Additional args to pass to the guest when starting it
        system_args = []
        system_args += ["-drive", f"file={self.seed_img},if=virtio,format=raw"]

        err = self.start(daemonize=False, extra_args=system_args)
        if err:
            log.error("failed starting...")
            return err

        return 0

    def init_using_bootimg(self):
        """Provision a guest OS using a boot image"""

        # Ensure the guest is *not* running
        self.kill()

        # Ensure the guest has a "home"
        self.initialize()

        # Ensure the guest has a cloudinit-image available for "installation"
        boot = self.cijoe.config.options["boot_images"].get(
            self.guest_config["boot_img"]
        )
        boot["img"] = Path(boot["img"]).resolve()

        if not boot["img"].exists():
            os.makedirs(boot["img"].parent, exist_ok=True)
            err, path = download(boot["url"], str(boot["img"]))
            if err:
                log.error(f"download({boot['url']}), {path}: failed")
                return err

        # Create the boot.img based on cloudinit_img
        shutil.copyfile(str(boot["img"]), str(self.boot_img))
        qemu_img(self.cijoe, f"resize {self.boot_img} 10G")

        return 0
