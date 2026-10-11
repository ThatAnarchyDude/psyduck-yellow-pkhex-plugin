# psyduck-yellow-pkhex-plugin

Pokémon Psyduck Yellow — PKHeX plugin.

Experimental compatibility work for the Pokémon Psyduck Yellow HeartGold ROM
hack. This plugin runs inside the standard PKHeX application; a separate
full editor is not required for the operations tested so far.

[Game development log](https://github.com/ThatAnarchyDude/corvus-workshop/blob/main/psyduck-yellow/DEVELOPMENT-LOG.md) ·
[PKHeX project fork](https://github.com/ThatAnarchyDude/PKHeX-Psyduck-Yellow) ·
[Experimental downloads](https://github.com/ThatAnarchyDude/psyduck-yellow-pkhex-plugin/releases)

## What it does

- Adds an explicitly selected Psyduck Yellow profile under Tools.
- Reads party Pokémon directly from the loaded save.
- Applies supported Hidden Abilities to the selected party slot, preserving
  its personality, gender, IVs and shiny status.
- Shows the project's shiny status correctly at XOR < 16. Stock Gen IV icons
  and legality checks still use official Gen IV rules.
- Reads and edits the player's ten PC item stacks, including names for the
  Shiny Charm and Friendship Charm. Quest and reward markers remain separate.

## Tested and still pending

The shared editing code passed save/export checks for 12 supported species,
including starter evolutions with abilities available in Generation IV.
Prepared Psyduck, Eevee and Togepi test saves, and a PC item edit, loaded through
Continue in the native DS emulator. Hidden Abilities, project shiny status,
Pokédex access and parcel progress were retained. No player ROM or save is
included in this repository.

The Windows DLL compiles with zero warnings/errors. A Windows host test passed plugin initialization, form construction, Tools menu
behavior, party selection, shiny display and PC gating. The pinned upstream PKHeX DLL loader also discovered and loaded the plugin
successfully on Windows. See the verified [Windows run](https://github.com/ThatAnarchyDude/corvus-workshop/actions/runs/38168315938). A complete manual Windows editing
session is still pending. Do not treat this as a fully validated editor.

Normal PKHeX Gen IV editing can replace a custom Hidden Ability with a normal
ability. Apply project abilities **after** other Pokémon edits, then export.
Do not Set a stale normal-editor Pokémon over a slot edited by this plugin.
The plugin does not change official legality checks, evolution legality, stock
species types or item menus. Espeon's Magic Bounce is unavailable in Gen IV.

## Build and use

Requires .NET SDK 10 and the pinned PKHeX 26.08.26 source. Run:

```sh
python scripts/build.py
```

The script verifies the upstream Git commit, builds Core and the plugin, and
writes an experimental source-and-binary ZIP under `artifacts/`. Windows users
can use the same command with Python and .NET installed.

Back up a normal battery save. Extract `PsyduckYellow.Plugin.dll` into the
`plugins` folder beside a matching PKHeX installation. Restart PKHeX, open a
copy of the save and select **Tools → Pokémon Psyduck Yellow**. Use
**File → Export SAV** after applying changes. Test the exported copy in-game
before replacing your regular save. Ordinary HGSS saves have the same format;
this plugin asks you to choose the hack profile rather than guessing.

To repeat the private save checks:

```sh
dotnet run --project src/PluginProbe -c Release -- copied-save.dsv private-output
```

## License and attribution

Plugin/probe source: GPL-3.0-or-later. See LICENSE. PKHeX is upstream software by
its contributors: https://github.com/kwsch/PKHeX. Its Core package declares the
same license. Keep notices and provide corresponding source when distributing
modified/combined work. The plugin package includes its source and license;
PKHeX binaries, game files, saves and access credentials are not bundled.

Report the plugin version, PKHeX version and what happened. Do not post ROMs,
save files, credentials or personal trainer identifiers in issues.
