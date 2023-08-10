cijoe-pkg-qemu: tools for systems development and testing
=========================================================

.. image:: https://img.shields.io/pypi/v/cijoe-pkg-qemu.svg
   :target: https://pypi.org/project/cijoe-pkg-qemu
   :alt: PyPI

.. image:: https://github.com/refenv/cijoe-pkg-qemu/workflows/selftest/badge.svg
   :target: https://github.com/refenv/cijoe-pkg-qemu/actions
   :alt: Build Status

This is a utility package for **cijoe**.

Please take a look at the documentation for how to install and use ``cijoe``:

* `Quickstart Guide`_
* `Usage`_

If you find bugs or need help then feel free to submit an `Issue`_. If you want
to get involved head over to the `GitHub page`_ to get the source code and
submit a `Pull request`_ with your changes.

FAQ
---

* Q: It fails starting qemu with the error: ``network backend 'user' is not compiled into this binary``.
* A: Then you probably need to install libslirp.

* Q: It fails starting qemu with the error: ``Could not set up host forwarding rule 'tcp::4200-:22'``.
* A: Then it is probably because something is already listening on port 4200 on
  the host.

.. _Quickstart Guide: https://cijoe.readthedocs.io/
.. _Usage: https://cijoe.readthedocs.io/
.. _GitHub page: https://github.com/refenv/cijoe-pkg-qemu
.. _Pull request: https://github.com/refenv/cijoe-pkg-qemu/pulls
.. _Issue: https://github.com/refenv/cijoe-pkg-qemu/issues
