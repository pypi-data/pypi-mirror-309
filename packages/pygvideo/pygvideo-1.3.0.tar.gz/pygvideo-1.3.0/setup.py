from distutils.core import setup

with open('README.md', 'r') as README:
    README_md = README.read()

setup(
    name = 'pygvideo',
    version = '1.3.0',
    description = 'pygvideo, video for pygame. Using moviepy video module to read and organize videos.',
    url = 'https://github.com/azzammuhyala/pygvideo.git',
    author = 'azzammuhyala',
    author_email = 'azzammuhyala@gmail.com',
    license = 'MIT',
    python_requires ='>=3.10',
    long_description_content_type = 'text/markdown',
    long_description = README_md,
    packages = ['pygvideo'], # find_packages(),
    install_requires = [
        "pygame>=2.5.0",
        "moviepy>=1.0.3"
    ],
    keywords = [
        'pygvideo', 'pygamevid', 'pyvidplayer', 'pygame vid', 'pygame video', 'video player', 'vid player',
        'pygame player', 'python pygame video', 'pgvideo', 'pgvid', 'video', 'player', 'pygame video player'
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)