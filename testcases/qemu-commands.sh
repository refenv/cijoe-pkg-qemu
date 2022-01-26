#!/bin/bash
#
# Show how 'cij.cmd' is routed to inside the qemu-guest
#
# Show how 'cij.cmd' is routed to inside the qemu-guest
#
# shellcheck disable=SC2119
#
CIJ_TEST_NAME=$(basename "${BASH_SOURCE[0]}")
export CIJ_TEST_NAME
# shellcheck source=modules/cijoe.sh
source "$CIJ_ROOT/modules/cijoe.sh"
test.enter

if hostname; then
  test.fail
fi

if ! cij.cmd "hostname"; then
  test.fail
fi

test.pass
