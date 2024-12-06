from setuptools import setup, find_packages

setup(
    name="clickshots",
    version="0.1.2",
    author="Akmol Masud",
    author_email="akmolmasud5@gmail.com",
    description="A robust automated screenshot capture system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pynput",
        "Pillow>=9.0.0",
        "pyscreenshot>=3.1",
        "python-xlib",
        "PyQt5; platform_system == 'Linux'",
        "pyautogui; platform_system == 'Darwin'",
    ],
    extras_require={
        'test': [
            'pytest>=7.0',
            'pytest-cov',
            'pytest-mock',
        ],
    },
    entry_points={
        "console_scripts": [
            "clickshots=clickshots.core:main",
        ],
    },
)