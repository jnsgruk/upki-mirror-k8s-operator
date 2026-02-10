#!/usr/bin/env python3
# Copyright Canonical Ltd.
# See LICENSE file for licensing details.

"""Utilities for running upki-mirror and nginx in Pebble."""

import os

import ops


def pebble_layer() -> ops.pebble.Layer:
    """Return a Pebble layer for managing UpkiMirror."""
    proxy_env = {
        "HTTP_PROXY": os.environ.get("JUJU_CHARM_HTTP_PROXY", ""),
        "HTTPS_PROXY": os.environ.get("JUJU_CHARM_HTTPS_PROXY", ""),
    }
    return ops.pebble.Layer(
        {
            "services": {
                "upki-mirror": {
                    "override": "replace",
                    "summary": "upki-mirror",
                    "command": "/bin/upki-mirror /var/www/html",
                    "startup": "enabled",
                    # We expect this process to run and exit with exit code 0, but
                    # exiting should not be considered a failure.
                    "on-success": "ignore",
                    "environment": proxy_env,
                },
                "nginx": {
                    "after": ["upki-mirror"],
                    "override": "replace",
                    "summary": "nginx",
                    "command": "nginx -g 'daemon off;'",
                    "startup": "enabled",
                },
            },
            "checks": {
                "up": {
                    "override": "replace",
                    "level": "alive",
                    "period": "30s",
                    "tcp": {"port": 80},
                    "startup": "enabled",
                },
                "fetch": {
                    "override": "replace",
                    "level": "alive",
                    "period": "360m",
                    "exec": {
                        "command": "/bin/upki-mirror /var/www/html",
                        "environment": proxy_env,
                    },
                    "startup": "enabled",
                },
            },
        }
    )
