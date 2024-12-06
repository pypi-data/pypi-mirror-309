from setuptools import setup, find_packages

setup(
    name="clickshots",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pynput",
        "Pillow",
        "pyautogui; platform_system == 'Darwin'",
    ],
    entry_points={
        "console_scripts": [
            "clickshots=clickshots.core:main",
        ],
    },
)