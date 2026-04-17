#!/usr/bin/env python3
# Copyright Canonical Ltd.
# See LICENSE file for licensing details.


from urllib.request import urlopen

import jubilant

from . import UPKI_MIRROR, retry


def test_deploy(juju: jubilant.Juju, upki_mirror_charm, upki_mirror_oci_image):
    juju.deploy(
        upki_mirror_charm, app=UPKI_MIRROR, resources={"nginx-image": upki_mirror_oci_image}
    )
    juju.wait(jubilant.all_active)


@retry(retry_num=10, retry_sleep_sec=3)
def test_revocation_manifest_was_fetched(juju: jubilant.Juju):
    output = juju.ssh(
        f"{UPKI_MIRROR}/0", "ls -l /var/www/html/revocation/manifest.json", container="nginx"
    ).strip()
    assert "/var/www/html/revocation/manifest.json" in output


@retry(retry_num=10, retry_sleep_sec=3)
def test_intermediates_manifest_was_fetched(juju: jubilant.Juju):
    output = juju.ssh(
        f"{UPKI_MIRROR}/0", "ls -l /var/www/html/intermediates/manifest.json", container="nginx"
    ).strip()
    assert "/var/www/html/intermediates/manifest.json" in output


@retry(retry_num=10, retry_sleep_sec=3)
def test_application_is_up(juju: jubilant.Juju):
    address = juju.status().apps[UPKI_MIRROR].units[f"{UPKI_MIRROR}/0"].address
    response = urlopen(f"http://{address}/revocation/manifest.json")
    assert response.status == 200

    response = urlopen(f"http://{address}/intermediates/manifest.json")
    assert response.status == 200
