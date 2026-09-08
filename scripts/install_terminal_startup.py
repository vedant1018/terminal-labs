#!/usr/bin/env python3
"""Package and install the repository's dependency-free VS Code startup extension."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

source = Path(__file__).resolve().parent.parent / '.devcontainer/terminal-startup'
package = json.loads((source / 'package.json').read_text())
manifest = f'''<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
 <Metadata>
  <Identity Language="en-US" Id="{package['name']}" Version="{package['version']}" Publisher="{package['publisher']}"/>
  <DisplayName>{package['displayName']}</DisplayName>
  <Description xml:space="preserve">{package['description']}</Description>
  <Properties>
   <Property Id="Microsoft.VisualStudio.Code.Engine" Value="{package['engines']['vscode']}"/>
   <Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="workspace"/>
  </Properties>
 </Metadata>
 <Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation>
 <Dependencies/>
 <Assets><Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/></Assets>
</PackageManifest>'''
content_types = '''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="json" ContentType="application/json"/>
 <Default Extension="js" ContentType="application/javascript"/>
 <Default Extension="vsixmanifest" ContentType="text/xml"/>
</Types>'''
with tempfile.TemporaryDirectory(prefix='terminal-lab-extension-') as directory:
    bundle = Path(directory) / 'terminal-lab-startup.vsix'
    with ZipFile(bundle, 'w', ZIP_DEFLATED) as archive:
        archive.writestr('extension.vsixmanifest', manifest)
        archive.writestr('[Content_Types].xml', content_types)
        for name in ('package.json', 'extension.js'):
            archive.write(source / name, f'extension/{name}')
    # During postCreate there is no connected editor / remote-cli IPC socket.
    # Use the installed server CLI directly, before the extension host starts.
    candidates = list(Path('/vscode/bin').glob('*/*/bin/code-server'))
    candidates += list((Path.home() / '.vscode-remote/bin').glob('*/bin/code-server'))
    candidates += list((Path.home() / '.vscode-server/bin').glob('*/bin/code-server'))
    if not candidates:
        raise RuntimeError('VS Code server installer was not found.')
    server = max(candidates, key=lambda path: path.stat().st_mtime)
    # Codespaces uses .vscode-remote, while standalone server CLI defaults to
    # .vscode-server. Install into the directory used by the attached host.
    remote_data = Path.home() / ('.vscode-remote' if os.environ.get('CODESPACES') == 'true' else '.vscode-server')
    subprocess.run([str(server), '--extensions-dir', str(remote_data / 'extensions'),
                    '--install-extension', str(bundle), '--force'], check=True)
print('Terminal Lab Startup installed.')
