#!/usr/bin/env python3
# Copyright Canonical Ltd.
# See LICENSE file for licensing details.


import jubilant
from pytest import mark

from . import UPKI_MIRROR

O11Y_CHARMS = ["loki-k8s"]
O11Y_RELS = ["log-proxy"]
ALL_CHARMS = [UPKI_MIRROR, *O11Y_CHARMS]


def test_deploy_charms(juju: jubilant.Juju, upki_mirror_charm, upki_mirror_oci_image):
    juju.deploy(
        upki_mirror_charm, app=UPKI_MIRROR, resources={"nginx-image": upki_mirror_oci_image}
    )

    for charm in O11Y_CHARMS:
        juju.deploy(charm, trust=True)

    juju.wait(jubilant.all_active, timeout=1000)


@mark.parametrize("endpoint,remote", list(zip(O11Y_RELS, O11Y_CHARMS)))
def test_create_relation(juju: jubilant.Juju, endpoint, remote):
    # Create the relation
    juju.integrate(f"{UPKI_MIRROR}:{endpoint}", remote)
    # Wait for the two apps to quiesce
    juju.wait(jubilant.all_active, timeout=1000)


# @mark.parametrize("endpoint,remote", list(zip(O11Y_RELS, O11Y_CHARMS)))
# def test_remove_relation(juju: jubilant.Juju, endpoint, remote):
#     # Remove the relation
#     juju.cli("remove-relation", f"{UPKI_MIRROR}:{endpoint}", remote)
#     # Wait for the two apps to quiesce
#     juju.wait(jubilant.all_active, timeout=1000)
