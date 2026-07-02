# Copyright Canonical Ltd.
# See LICENSE file for licensing details.

import importlib.util
import subprocess
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "tests.integration.conftest", Path(__file__).parents[1] / "integration" / "conftest.py"
)
assert spec is not None
integration_conftest = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(integration_conftest)


def test_traefik_service_ip_uses_loadbalancer_ip_without_shell_quotes():
    commands = []

    def run(cmd, **kwargs):
        commands.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, stdout="10.0.0.12", stderr="")

    assert integration_conftest._traefik_service_ip("testing", run=run, attempts=1) == "10.0.0.12"

    assert commands == [
        [
            "/snap/bin/kubectl",
            "-n",
            "testing",
            "get",
            "service",
            "traefik-k8s-lb",
            "-o=jsonpath={.status.loadBalancer.ingress[0].ip}",
        ]
    ]


def test_traefik_service_ip_falls_back_to_cluster_ip():
    responses = iter(["", "", "10.152.183.45"])
    sleeps = []

    def run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout=next(responses), stderr="")

    assert (
        integration_conftest._traefik_service_ip(
            "testing", run=run, sleep=sleeps.append, attempts=2, delay=5
        )
        == "10.152.183.45"
    )
    assert sleeps == [5]


def test_traefik_service_ip_fails_clearly_without_service_address():
    def run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    with pytest.raises(RuntimeError, match="no LoadBalancer IP or ClusterIP"):
        integration_conftest._traefik_service_ip(
            "testing", run=run, sleep=lambda _: None, attempts=1
        )
