# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gamesnake.py'],
    pathex=['C:\Users\user\OneDrive\Bureau\game sanke'],
    binaries=[],
    datas=[
        ('GIF/head_up.png', 'GIF'),
        ('GIF/head_down.png', 'GIF'),
        ('GIF/head_right.png', 'GIF'),
        ('GIF/head_left.png', 'GIF'),
        ('GIF/tail_up.png', 'GIF'),
        ('GIF/tail_down.png', 'GIF'),
        ('GIF/tail_right.png', 'GIF'),
        ('GIF/tail_left.png', 'GIF'),
        ('GIF/body_vertical.png', 'GIF'),
        ('GIF/body_horizontal.png', 'GIF'),
        ('GIF/body_tr.png', 'GIF'),
        ('GIF/body_tl.png', 'GIF'),
        ('GIF/body_br.png', 'GIF'),
        ('GIF/body_bl.png', 'GIF'),
        ('GIF/apple3.jpg', 'GIF'),
        ('crunch.mp3', '.'),
        ('Winter Minie.ttf', '.'),
        ('snake.png', '.'),
        ('users.db', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='game',
)