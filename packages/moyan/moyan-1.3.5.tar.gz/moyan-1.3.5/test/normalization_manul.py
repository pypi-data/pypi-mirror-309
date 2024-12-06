#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   normalization_manul.py
@Time    :   2023/09/22 10:41:15
@Author  :   moyan 
@Contact :   ice_moyan@163.com
'''
import os
import torch
import numpy as np
import torch.nn as nn
torch.manual_seed(42)

def BN(inputs):
    ''''
        use torch
    '''
    c = inputs.shape[1]
    epsilon = 1e-5
    # print(c)
    for i in range(c):
        channel = inputs[:,i,:,:]
        mean = torch.Tensor.mean(channel)
        var = torch.Tensor.var(channel,False)
        channel_new = ((channel - mean)  /   (torch.pow(var + epsilon, 0.5))  )  * 1 + 0
        inputs[:,i,:,:] = channel_new
    return inputs


def BN2(inputs: np.ndarray):
    ''''
        use numpy
    '''
    epsilon = 1e-5
    n, c, h, w = inputs.shape
    x = inputs.transpose((1, 0, 2, 3)) # c, n, h, w
    x = x.reshape(c, n*h*w) # c, n*h*w
    mu1 = x.mean(axis=1).reshape(1, c, 1, 1)
    std1 = x.std(axis=1).reshape(1, c, 1, 1)
    y = (inputs - mu1) / (std1+epsilon)
    return y


def LN2(inputs: np.ndarray):
    epsilon = 1e-5
    n, c, h, w = inputs.shape
    x = inputs.reshape(n, c*h*w) # c, n*h*w
    mu1 = x.mean(axis=1).reshape(n, 1, 1, 1)
    std1 = x.std(axis=1).reshape(n, 1, 1, 1)
    y = (inputs - mu1) / (std1+epsilon)
    return y


def IN(inputs: np.ndarray):
    '''
    Instance Normalization (IN) 最初用于图像的风格迁移。
    作者发现，在生成模型中， feature map 的各个 channel 
    的均值和方差会影响到最终生成图像的风格，因此可以先把
    图像在 channel 层面归一化，然后再用目标风格图片对应 
    channel 的均值和标准差“去归一化”，以期获得目标图片的风格
    。IN 操作也在单个样本内部进行，不依赖 batch。对于  
    ，IN 对每个样本的 H、W 维度的数据求均值和标准差，
    保留 N 、C 维度，也就是说，它只在 channel 内部求
    均值和标准差
    '''
    epsilon = 1e-5
    n, c, h, w = inputs.shape
    x = inputs.reshape(n*c, h*w) # n*c, h*w
    mu1 = x.mean(axis=1).reshape(n, c, 1, 1)
    std1 = x.std(axis=1).reshape(n, c, 1, 1)
    y = (inputs - mu1) / (std1+epsilon)
    return y

def GN(inputs: np.ndarray):
    '''
    Group Normalization (GN) 适用于占用显存比较大的任务，
    例如图像分割。对这类任务，可能 batchsize 只能是个位数，
    再大显存就不够用了。而当 batchsize 是个位数时，
    BN 的表现很差，因为没办法通过几个样本的数据量，
    来近似总体的均值和标准差。GN 也是独立于 batch 的，
    它是 LN 和 IN 的折中。GN 计算均值和标准差时，
    把每一个样本 feature map 的 channel 分成 G 组，
    每组将有 C/G 个 channel，然后将这些 channel 
    中的元素求均值和标准差。各组 channel 用其对应的
    归一化参数独立地归一化
    '''
    g = 2 # group
    epsilon = 1e-5
    n, c, h, w = inputs.shape
    x = inputs.reshape(n, g, -1) # n, g, c/g*h*w
    mu1 = x.mean(axis=1).reshape(n, g, 1, 1)
    std1 = x.std(axis=1).reshape(n, g, 1, 1)
    y = (inputs - mu1) / (std1+epsilon)
    y = y.reshape(n, c, h, w)
    return y



def test_bn():
    torch_bn = nn.BatchNorm2d(3)
    x = (torch.randn(1, 3, 2, 2)) *10
    print(x)

    y1 = BN(x.detach())
    y2 = torch_bn(x)
    print(y1)
    print(y2)


    y3 = BN2(x.numpy())
    print(y3)
 
def test_ln():

    torch_ln = nn.LayerNorm([3, 2, 2])
    x = torch.randn(1, 3, 2, 2) * 10
    print(x)

    # Manually apply Layer Normalization
    y2 = torch_ln(x)
    y3 = LN2(x.numpy())

    print(y2)
    print(y3)


def main():
    # test_bn()
    test_ln()


if __name__=='__main__':
    main()
