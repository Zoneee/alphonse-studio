#!/usr/bin/env python3
"""Install / uninstall / verify the ponytail plugin for a DSH profile.

ponytail ships a prompt pack that makes a coding agent follow a
seven-rung "do less" ladder. This script wraps `dsh plugin add` /
`dsh plugin remove` so the install recipe lives next to the docs in
this repo instead of being retyped on every machine.

Conventions
-----------
* One script per plugin, named after the plugin.
* Subcommands: install, uninstall, status, verify.
* `install` is the only command that mutates DSH state.
* `verify` only inspects the filesystem; safe to run any time.
* Defaults to profile `web`. Override with `--profile <name>`.

The script is intentionally small. Anything beyond subcommand dispatch
belongs in a sibling helper, not here.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PLUGIN_NPM = "@mengyuly/dsh-ponytail"
PLUGIN_GH = "github:MengYuil/dsh-ponytail"
DEFAULT_PROFILE = "web"


def _check_dsh() -> None:
    """Refuse to run if `dsh` is not on PATH."""
    if shutil.which("dsh") is None:
        sys.exit("error: `dsh` not found on PATH. Install DSH first.")


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a command, raise on failure, return CompletedProcess."""
    result = subprocess.run(cmd, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout or "")
        sys.exit(f"error: command failed: {' '.join(cmd)}")
    return result


def _plugin_dir(profile: str) -> Path:
    return Path.home() / ".dsh" / "profiles" / profile / "node_modules" / "@mengyuly" / "dsh-ponytail"


def cmd_install(profile: str, source: str) -> None:
    _check_dsh()
    if _plugin_dir(profile).exists():
        print(f"ponytail already installed for profile '{profile}'. Run `status` or `uninstall` first.")
        sys.exit(0)
    print(f"Installing {source} into profile '{profile}'...")
    _run(["dsh", "plugin", "--profile", profile, "add", source])
    print("Done. Restart `dsh web` (or the relevant profile) to load the new skills.")


def cmd_uninstall(profile: str) -> None:
    _check_dsh()
    if not _plugin_dir(profile).exists():
        print(f"ponytail not installed for profile '{profile}'. Nothing to do.")
        sys.exit(0)
    print(f"Uninstalling ponytail from profile '{profile}'...")
    _run(["dsh", "plugin", "--profile", profile, "remove", PLUGIN_NPM])
    print("Done. Restart the profile to unload the skills.")


def cmd_status(profile: str) -> None:
    installed = _plugin_dir(profile).exists()
    pkg = Path.home() / ".dsh" / "profiles" / profile / "package.json"
    in_manifest = False
    if pkg.exists():
        in_manifest = PLUGIN_NPM in pkg.read_text()
    state = "installed" if installed else "absent"
    manifest = "listed" if in_manifest else "missing"
    print(f"profile: {profile}")
    print(f"plugin dir: {'present' if installed else 'absent'}  ({_plugin_dir(profile)})")
    print(f"manifest entry: {manifest}  ({pkg})")
    print(f"state: {state}")


def cmd_verify(profile: str) -> None:
    """Filesystem-only check. No DSH state mutation."""
    errors = []
    pdir = _plugin_dir(profile)
    if not pdir.exists():
        errors.append(f"plugin dir missing: {pdir}")
    else:
        for required in ("lib/index.js", "lib/invariant.js", "package.json", "cordis.patch.yml"):
            if not (pdir / required).exists():
                errors.append(f"missing file: {pdir / required}")
    pkg = Path.home() / ".dsh" / "profiles" / profile / "package.json"
    if not pkg.exists():
        errors.append(f"profile package.json missing: {pkg}")
    elif PLUGIN_NPM not in pkg.read_text():
        errors.append(f"{PLUGIN_NPM} not declared in {pkg}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        sys.exit(1)
    print(f"OK: ponytail verified for profile '{profile}'.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE,
        help=f"DSH profile name (default: {DEFAULT_PROFILE})",
    )
    sub = parser.add_subparsers(dest="action", required=True)

    p_install = sub.add_parser("install", help="install the plugin via dsh plugin add")
    p_install.add_argument(
        "--source",
        default=PLUGIN_GH,
        help=f"install source (default: {PLUGIN_GH})",
    )

    sub.add_parser("uninstall", help="remove the plugin via dsh plugin remove")
    sub.add_parser("status", help="report install state without changing anything")
    sub.add_parser("verify", help="filesystem-only check, no DSH state mutation")

    args = parser.parse_args()
    dispatch = {
        "install": lambda: cmd_install(args.profile, args.source),
        "uninstall": lambda: cmd_uninstall(args.profile),
        "status": lambda: cmd_status(args.profile),
        "verify": lambda: cmd_verify(args.profile),
    }
    dispatch[args.action]()


if __name__ == "__main__":
    main()