# Hardware modules

Each module owns its CAD, electronics, firmware/software, simulations, documentation, references and
renders. These folders hold local working copies; MiniPLM stores saved deliverables
and revision history. No hardware module or MiniPLM target has been specified yet.

The repository-root [project specification](../../SPECIFICATION.md) defines the
overall goal. Each module's root `SPECIFICATION.md` traces its requirements to
that approved project baseline; complete and approve the affected module spec
before implementation. A new scaffold is a draft, not authorization to develop.
Both specs track the [PLM lifecycle](../docs/plm-lifecycle.md) and actual owner
stage sign-offs. Each generated module starts with all stages `NOT_STARTED`.

The MiniPLM project is the product, not a directory. The local
`user/modules/<module>/` folder maps to `<module>/` within its selected iteration,
for example `wheel/SPECIFICATION.md` and `wheel/cad/`. Omit only the local
`user/modules/` wrapper in PLM, preserving the module name and discipline folders.

See [the project rules](../docs/project-rules.md) for the layout. To start one:

```sh
python3 agent/scripts/new_module.py wheel
```

`wheel` is an example. The command creates module folders, a readable index and a
draft root `SPECIFICATION.md`. Complete the specification and record actual
approval for the agreed scope before module implementation starts. Creating the
scaffold does not approve any requirements or authorize development. Use
`--components` to add separate CAD component and matching STEP folders when needed.
It does not create a MiniPLM product, iteration or folder. Resolve the downstream
target through the [repository workflow](../../agent/skills/miniplm/SKILL.md)
before saving hardware deliverables.

Use `--firmware` and/or `--software` to add those source roots. Create a named
target/app folder when its work starts. Within each module, group electrical
files by board, Blender assets by scene and simulation inputs/reports by study.
See the [publish policy](../../agent/skills/miniplm/references/publish-policy.md)
for native/STEP pairs, required dependencies and files that must stay local.

If MiniPLM or a usable target is unavailable, these directories are the fallback.
Report that files are local-only without PLM version control or revision history.
