# -*- mode: python ; coding: utf-8 -*-

# Manually adding datas
datas = [
    (os.path.join('src', 'app', 'tasks'), 'tasks'),
    (os.path.join('src', 'app', 'ai'), 'ai'),
]

# Manually adding hidden imports
hiddenimports = []
with open('requirements.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if not line.startswith('#'):
            hiddenimports.append(line)
hiddenimports.extend(['pydicom.encoders.gdcm', 'pydicom.encoders.pylibjpeg'])
print(hiddenimports)

a = Analysis(
    ['src\\app\\main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
