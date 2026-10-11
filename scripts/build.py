#!/usr/bin/env python3
"""Build against the verified upstream commit; package source and plugin only."""
import json,subprocess,zipfile,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
up=json.loads((root/'upstream.json').read_text());dep=root/'.deps/PKHeX'
def run(*args):subprocess.run(args,cwd=root,check=True)
if not dep.exists():
 dep.parent.mkdir(exist_ok=True)
 run('git','clone','--filter=blob:none','--no-checkout',up['repository'],str(dep))
run('git','-C',str(dep),'fetch','--depth=1','origin',up['commit'])
run('git','-C',str(dep),'checkout','--detach',up['commit'])
actual=subprocess.check_output(['git','-C',str(dep),'rev-parse','HEAD'],text=True).strip()
if actual!=up['commit']:raise RuntimeError('Unexpected upstream revision')
# Do not build edited dependency code while describing it as the pinned revision.
if subprocess.check_output(['git','-C',str(dep),'status','--porcelain'],text=True).strip():
 raise RuntimeError('Upstream dependency contains modifications')
run('dotnet','build',str(dep/'PKHeX.Core/PKHeX.Core.csproj'),'-c','Release','--nologo')
run('dotnet','build','src/PsyduckYellow.Plugin','-c','Release','--nologo')
run('dotnet','build','src/PluginProbe','-c','Release','--nologo')
run('dotnet','build','src/WindowsHostProbe','-c','Release','--nologo')
binary=root/'src/PsyduckYellow.Plugin/bin/Release/net10.0-windows/PsyduckYellow.Plugin.dll'
art=root/'artifacts';art.mkdir(exist_ok=True)
package=art/'PsyduckYellow.Plugin-0.1.0-experimental.zip'
# Deterministic timestamps, never include .deps, saves or ROMs.
files=[root/'README.md',root/'LICENSE',root/'upstream.json',root/'Directory.Build.props',root/'.gitignore',root/'validation.json',root/'.github/workflows/build.yml']
files+=sorted((root/'src').rglob('*.cs'))+sorted((root/'src').rglob('*.csproj'))+sorted((root/'scripts').rglob('*.py'))
files=[p for p in files if not {'bin','obj'}.intersection(p.relative_to(root).parts)]
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as archive:
 for p in files+[binary]:
  name='PsyduckYellow.Plugin.dll' if p==binary else 'source/'+str(p.relative_to(root))
  info=zipfile.ZipInfo(name,(2026,10,11,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
  archive.writestr(info,p.read_bytes())
(art/'SHA256SUMS').write_text(hashlib.sha256(package.read_bytes()).hexdigest()+'  '+package.name+'\n')
print(package)
