# -*- mode: python ; coding: utf-8 -*-
# Arquivo de especificação para PyInstaller
# Use: pyinstaller build.spec

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('database/schema.sql', 'database'),
        ('ui/resources', 'ui/resources'),
    ],
    hiddenimports=[
        'PySide6',
        'sqlite3',
    ] + collect_submodules('PySide6'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Sistema_Estoque',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # True = janela de console, False = sem console (modo GUI)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
