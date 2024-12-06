# tf-registry

A client for the public Terraform registry.

## Usage

```py
from tf_registry import RegistryClient

client = RegistryClient()

# List modules
print(client.list())
```

This client implements the APIs documented here:

<https://developer.hashicorp.com/terraform/registry/api-docs>

For more details, peruse the docstrings.

## Development

This project uses [uv](https://docs.astral.sh/uv/) and
[just](https://github.com/casey/just). The `justfile` should contain most of
what you need - including `just format`, `just lint`, `just check`, and
`just test`. Note that type checking requires node.js, because I use pyright.

## License

MIT. See `LICENSE` for more details.
