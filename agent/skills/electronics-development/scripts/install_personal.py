#!/usr/bin/env python3
"""Install this skill by symlink and add a scoped persistent instruction, preserving other text."""
import os
import argparse
from pathlib import Path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--replace-link-from', type=Path, help='Explicitly migrate symlinks pointing to this old source only')
args=parser.parse_args()
source=Path(__file__).resolve().parents[1]
codex=Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex')))
links=[codex/'skills/electronics-development',Path.home()/'.agents/skills/electronics-development']
for link in links:
    if link.exists() or link.is_symlink():
        if link.resolve()!=source and not (link.is_symlink() and args.replace_link_from and link.resolve()==args.replace_link_from.resolve()):
            raise SystemExit(f'Refusing to replace an existing skill: {link}')
agent=codex/'AGENTS.md'
start='<!-- electronics-development:start -->'
end='<!-- electronics-development:end -->'
block=f'''{start}
## Electronics development
For circuit, PCB, component, hardware-facing firmware, electrical simulation and board-release work, load and follow $electronics-development (installed at {links[0]}/SKILL.md). Use change-specific engineering checks and current evidence. Draft development may continue with explicit blockers; do not claim prototype manufacture, powered load testing or qualified operation is ready until the corresponding release gate passes. Keep physical measurements distinct from calculations/simulations. Apply this rule only to electronics work, not unrelated software, presentation-only edits or mechanical CAD. The skill does not authorize ordering or physical test actions.
{end}'''
old=agent.read_text() if agent.exists() else ''
if (start in old)!=(end in old):
    raise SystemExit('Incomplete existing instruction block; refusing to modify')
if start in old:
    before,rest=old.split(start,1);_,after=rest.split(end,1)
    new=before+block+after
else:
    new=old.rstrip()+('\n\n' if old.strip() else '')+block+'\n'
if new!=old and agent.exists() and agent.with_name('AGENTS.md.electronics-development.bak').exists():
    raise SystemExit('Instruction backup already exists; refusing to overwrite')
for link in links:
    link.parent.mkdir(parents=True,exist_ok=True)
    if link.is_symlink() and link.resolve()!=source:
        link.unlink()
    if not link.is_symlink():link.symlink_to(source,target_is_directory=True)
agent.parent.mkdir(parents=True,exist_ok=True)
if new!=old:
    if agent.exists():
        backup=agent.with_name('AGENTS.md.electronics-development.bak')
        if backup.exists():raise SystemExit(f'Backup already exists: {backup}; refusing to overwrite')
        backup.write_text(old)
    agent.write_text(new)
print('Skill source:',source)
for link in links:print('Discovery link:',link,'->',link.resolve())
print('Persistent rule:',agent)
print('Open a new Codex session to load the persistent rule; restart if the skill is not listed.')
