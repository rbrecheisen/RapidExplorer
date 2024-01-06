# -*- mode: python ; coding: utf-8 -*-

# Manually adding tasks package
task_files = [(os.path.join('src', 'app', 'tasks'), 'tasks')]

a = Analysis(
    ['src\\app\\main.py'],
    pathex=[],
    binaries=[],
    datas=task_files,
    hiddenimports=['pydicom.encoders.gdcm', 'pydicom.encoders.pylibjpeg', 'numpy'],
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
