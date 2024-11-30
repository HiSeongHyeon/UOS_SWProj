# -*- mode: python ; coding: utf-8 -*-

import os  # os 모듈을 사용하기 위해 import 추가
import sys  # 필요한 경우 sys도 import
from PyInstaller.utils.hooks import collect_data_files  # PyInstaller의 유틸리티 함수 사용을 위해 import

block_cipher = None

mediapipe_data_files = collect_data_files('mediapipe')


a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('config.py', '.'),('config.py', '.'),('HPE/*.py', 'HPE'),('UI/*.py', 'UI'),('UI/img/*', 'UI/img'),] + mediapipe_data_files,
    hiddenimports=['sqlite3'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='doheoi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['UI\\img\\logo.ico'],
)
