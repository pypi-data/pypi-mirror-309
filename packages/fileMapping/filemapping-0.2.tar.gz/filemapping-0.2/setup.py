from setuptools import setup, find_packages



# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='fileMapping',
    version='0.2',
    author='朝歌夜弦',
    author_email='bop-lp@qq.com',
    description='用于快速调用文件夹下的py文件或者包',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/bop-lp/fileMapping",
    packages=find_packages(),
    install_requires=[]
)

"""
pypi-AgEIcHlwaS5vcmcCJGEyNTdiMzNlLWYwODAtNDdmNS04YWQ4LWM3OTY4MTlkMTdiNgACKlszLCI1MDlmZDVjYi1iMWM3LTRiNDItOWJlMy1hNGZkODljZGRhNjIiXQAABiB_ptg4hWHus3i546XFksUURpHHpPU-qmmbpk643IDVTQ
"""
