#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   load_modelscope_data.py
@Time    :   2024/10/23 09:10:11
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
from modelscope.msdatasets import MsDataset

def main():
    data_dir = "~/DataSet/modelscope/refcoco/"
    # ds =  MsDataset.load('swift/refcoco', data_dir=data_dir)
    ds =  MsDataset.load(data_dir)
    print(ds)

    print(next(iter(ds['train'])))

if __name__=='__main__':
    main()
