from setuptools import setup

APP = ['linalgpy.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleName': 'MyApp',
        'CFBundleDisplayName': 'My Application',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'Miaomiaomiao',
    },
    'packages': ['tkinter'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)