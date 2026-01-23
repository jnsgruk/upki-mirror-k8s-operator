# upki-mirror Operator

This repository contains the source code for a Charmed Operator that drives [upki-mirror] on Kubernetes.

## Usage

Assuming you have access to a bootstrapped Juju controller on Kubernetes, you can simply:

```bash
$ juju deploy upki-mirror-k8s
```

You can see the application address in `juju status`, or get it like so:

```bash
$ juju status --format=json | jq -r '.applications."upki-mirror-k8s".address'
```

You should then be able to browse to `http://<address>/manifest.json`.

## OCI Images

This charm relies on a [Chiselled ROCK](https://ubuntu.com/blog/combining-distroless-and-ubuntu-chiselled-containers).

This image is similar to a `distroless` image, in that it only contains the bare minimum
dependencies for upki-mirror to run. You can see the source [here](./rockcraft.yaml).

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines
on enhancements to this charm following best practice guidelines, and the
[contributing] doc for developer guidance.

[contributing]: https://github.com/jnsgruk/upki-mirror-k8s-operator/blob/main/CONTRIBUTING.md
