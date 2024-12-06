from setuptools import setup
from rft.version import __version__
desc = 'Manage tmux sessions & windows via Rofi'

setup(
    name='rofi-tmux-ng',
    version=__version__,
    description=desc,
    author='Laurito',
    author_email='viniarck@gmail.com',
    keywords='rofi tmux tmuxinator i3 manage switch',
    url='http://github.com/viniarck/rofi-tmux',
    packages=['rft', 'rft/bin'],
    license='MIT',
    install_requires=['python-rofi==1.0.1', 'i3ipc>=2.0.1', 'click', 'tendo'],  # cloup
    python_requires='>=3.11',
    entry_points='''
        [console_scripts]
        rft=rft.bin.main_client:main
        rofi-tmux=rft.bin.main_client:main
        rft-daemon=rft.bin.main_daemon:main
    ''',
)
