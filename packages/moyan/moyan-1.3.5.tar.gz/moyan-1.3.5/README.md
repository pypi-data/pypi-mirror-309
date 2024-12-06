# Moyan

#### 介绍
python toollib


#### 安装教程

1.  pip install moyan

#### 使用说明

1. python setup.py build   编译

2. python setup.py sdist   打包到本地

3. python setup.py install 本地安装

4.  touch ~/.pypirc 配置pypi账号
    
    ```
    [distutils]
    index-servers = pypi
     
    [pypi]
    repository = https://upload.pypi.org/legacy/
    username = __token__
    password = pypi-AgEIcHlwaS5vcmcCJGUwNGI1OGIxLTA5N2ItNDMzZS05MTJmLWE2MjE1MjE4NTk4NgACDVsxLFsibW95YW4iXV0AAixbMixbImUzZDkwYmNiLWZhNTEtNGIyZS1hNWExLWFjNDBiYTY5ZTc0NSJdXQAABiDot-v0eotAIMjC0NqPR3ta69HVUSbIvr8SkpUoxFgaNA
    ```
    
5. twine upload dist/* 上传

6.  pip install moyan

#### TODO

- [ ] Converte VOC data to tfrecords
- [ ] Convert data to lmdb
- [ ] Pytorch data augmentation

#### Acknowledgements

- [hanrancode](https://github.com/hanranCode)