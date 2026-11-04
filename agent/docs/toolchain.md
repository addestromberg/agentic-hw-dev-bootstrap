# Toolchain and MCP maintenance

FreeCAD, KiCad and Blender are installed and maintained with pacman. The user
completed the system installation during setup. The observed package versions are
FreeCAD `1.1.4-3`, KiCad `10.0.7-2`, Blender `17:5.2.3-5` (application 5.2.3 LTS),
and `kicad-library` `10.0.7-1`.

## Integrations

| Codex server | Upstream | Configured operation |
| --- | --- | --- |
| `rsim_freecad` | [neka-nat/freecad-mcp](https://github.com/neka-nat/freecad-mcp) | `execute_code_headless` using pacman's `freecadcmd` |
| `rsim_kicad` | [Seeed-Studio/kicad-mcp-server](https://github.com/Seeed-Studio/kicad-mcp-server) | Schematic/PCB tools, native `pcbnew`, `kicad-cli` checks/exports |
| `rsim_blender` | [djeada/blender-mcp-server](https://github.com/djeada/blender-mcp-server) | Headless Python, jobs and rendering; pass `transport="headless"` |

MiniPLM repository operations use the separate `miniplm` MCP tools when connected.
Follow the [repository skill](../skills/miniplm/SKILL.md) for project/iteration
selection, revision handling and file-transfer limits. That integration is not
installed by `setup_mcp.py` or exercised by `verify_toolchain.py`. Its connection
and credentials belong to the target environment; this bootstrap does not assign
a MiniPLM account, product or iteration. Tool availability alone does not establish
that authentication, binary retrieval or uploads work.
When the integration/session or a usable target is unavailable, use the same
local deliverable hierarchy and report local-only storage without PLM version
control/history. Local engineering work does not require setting up MiniPLM.

The [PLM lifecycle](../../user/docs/plm-lifecycle.md) is represented by readable
project/module specification records and stage reviews. Available MiniPLM tools
can inspect project stages and use existing upload containers, but do not expose
a general stage-transition or approval operation. No lifecycle server automation
has been installed or qualified by this bootstrap. Existing engineering checker
stage names and schemas remain unchanged.

The configured FreeCAD and Blender tools do not need an open GUI or GUI addon.
Their upstream servers may log a missing optional GUI bridge at startup; headless
tools run independently. GUI-only tools are excluded from the FreeCAD and Blender
tool lists. KiCad's schematic editing tools are experimental upstream; check
connectivity and run relevant ERC/DRC after changes.

The MCP packages use isolated Python environments under `agent/objects/envs/`.
`agent/scripts/run_mcp.py` selects the environment and redirects temporary,
configuration, cache and application-data paths into `agent/objects/runtime/`.
For KiCad it exposes pacman's Python bindings and selects `/usr/bin/python3` for
native helper subprocesses. For FreeCAD it redirects the upstream headless
temporary-script directory, which otherwise hardcodes a user-home cache path.
It does not change the user's HOME.

The Blender launcher sets `BLENDER_SYSTEM_PYTHON=/usr` so Arch Blender uses
pacman's standard library rather than the separate uv Python found on the user's
PATH. That prefix override resolved missing `math`/`_posixsubprocess` imports in
the initial headless render attempt. The variable is documented in Blender's
[command-line reference](https://docs.blender.org/manual/en/5.4/advanced/command_line/arguments.html).

Pass absolute paths to MCP tools. Put module deliverables in the module's user
folders and scripts/evidence/scratch in its agent folders, following
[project rules](../../user/docs/project-rules.md). Default tool output paths are
not a substitute for selecting the correct owning directory.

## Configuration and restart

The maintained MCP settings are in [codex.toml](../config/codex.toml).
`.codex/config.toml` links to that file. The same three server entries have been
registered in the user's `~/.codex/config.toml`; `codex mcp list` confirmed them.
Existing unrelated entries were preserved. The CLI inspection did not discover
the project-only entries during setup, so user-level registration is the verified
loading route here. These user-level entries therefore also appear in other
projects and point back to this workspace.

`.agents/skills` links to `agent/skills/`. It exposes five adapted engineering
skills plus `hardware-documentation` and `miniplm`. Restart the session from this workspace to
load the new servers and skills. See the official
[MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) and
[local skill discovery](https://learn.chatgpt.com/docs/build-skills) documentation.

To change launch settings, update the maintained TOML and the corresponding
`rsim_*` entries in the user's Codex configuration. The settings contain local
absolute paths; update those if the project moves. Do not copy credentials into
the repository.

## Rebuild and check

Upstream source commits are pinned in [mcp-sources.json](../config/mcp-sources.json).
Dependency versions observed during installation are recorded in
`agent/evidence/setup/*-mcp-packages.json`; the rebuild script uses the pinned
server source with its declared dependency constraints, rather than a complete
transitive dependency lock.

```sh
python3 agent/scripts/setup_mcp.py
python3 agent/scripts/verify_toolchain.py
```

The setup script needs network access when dependencies are missing. It refuses
to overwrite a source checkout that differs from the pinned clean baseline.
After a system Python ABI upgrade, recreate the disposable environments under
`agent/objects/envs/` and run setup again.

The verification script builds/reopens a simple native parametric FreeCAD box,
exports STEP, creates a KiCad project and outline, obtains board statistics,
runs DRC, exports Gerbers, and saves/renders a small Blender scene on CPU. Check
`agent/evidence/setup/toolchain-verification.json` for the latest completed result
and timestamped records for individual calls. Smoke artifacts stay under
`agent/objects/toolchain-check/` and are excluded from Git.

These checks validate the software path. They do not validate a cockpit design,
manufacturing readiness, material properties or a simulation solver. Optional FEM,
thermal and other solvers have not been qualified by this setup.

## Skill provenance

The five engineering skills were copied byte-for-byte from
[`addestromberg/skywatch`](https://github.com/addestromberg/skywatch) at commit
`76e3701c226106dc3da5e415741ea417a42b4e1d`. All 25 copied files matched their Git
blob hashes. The import manifest is in `agent/evidence/setup/skywatch-import.json`.
The project-local documentation skill was created for RSIM. All six skills passed
the skill creator's structural validator.

That manifest describes the original import, not the current skill contents.
The engineering skills have since been adapted for the MiniPLM repository workflow
and reusable project scope. `miniplm` is a project-local skill; downstream target
mappings and design revisions are intentionally absent from the template.

An initial Conda installation was discarded when the user selected pacman.
Its local environment and downloaded package cache were removed. Small setup
logs retain the history; the active toolchain uses the pacman applications.
