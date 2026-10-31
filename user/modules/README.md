# Hardware modules

Each module owns its CAD, electronics, simulations, documentation, references and
renders. No hardware module has been specified yet.

See [the project rules](../docs/project-rules.md) for the layout. To start one:

```sh
python3 agent/scripts/new_module.py wheel
```

`wheel` is an example. The command creates module folders and a readable index;
separate CAD component folders are added when needed.
