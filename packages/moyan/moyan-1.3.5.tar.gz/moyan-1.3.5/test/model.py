# Mobile UNet and Inverted Residual Block
# Author: Lafith Mattara
# Date: July 2022


import torch
import torch.nn as nn
import torch.nn.functional as F

class InvertedResidualBlock(nn.Module):
    """
    inverted residual block used in MobileNetV2
    """
    def __init__(self, in_c, out_c, stride, expansion_factor=6, deconvolve=False):
        super(InvertedResidualBlock, self).__init__()
        # check stride value
        assert stride in [1, 2]
        self.stride = stride
        self.in_c = in_c
        self.out_c = out_c
        # Skip connection if stride is 1
        self.use_skip_connection = True if self.stride == 1 else False

        # expansion factor or t as mentioned in the paper
        ex_c = int(self.in_c * expansion_factor)
        if deconvolve:
            self.conv = nn.Sequential(
                # pointwise convolution
                nn.Conv2d(self.in_c, ex_c, 1, 1, 0, bias=False),
                nn.BatchNorm2d(ex_c),
                nn.ReLU6(inplace=True),
                # depthwise convolution
                nn.ConvTranspose2d(ex_c, ex_c, 4, self.stride, 1, groups=ex_c, bias=False),
                nn.BatchNorm2d(ex_c),
                nn.ReLU6(inplace=True),
                # pointwise convolution
                nn.Conv2d(ex_c, self.out_c, 1, 1, 0, bias=False),
                nn.BatchNorm2d(self.out_c),
            )
        else:
            self.conv = nn.Sequential(
                # pointwise convolution
                nn.Conv2d(self.in_c, ex_c, 1, 1, 0, bias=False),
                nn.BatchNorm2d(ex_c),
                nn.ReLU6(inplace=True),
                # depthwise convolution
                nn.Conv2d(ex_c, ex_c, 3, self.stride, 1, groups=ex_c, bias=False),
                nn.BatchNorm2d(ex_c),
                nn.ReLU6(inplace=True),
                # pointwise convolution
                nn.Conv2d(ex_c, self.out_c, 1, 1, 0, bias=False),
                nn.BatchNorm2d(self.out_c),
            )
        self.conv1x1 = nn.Conv2d(self.in_c, self.out_c, 1, 1, 0, bias=False)

            

    def forward(self, x):
        if self.use_skip_connection:
            out = self.conv(x)
            if self.in_c != self.out_c:
                x = self.conv1x1(x)
            return x+out
        else:
            return self.conv(x)


class MobileUNet(nn.Module):
    """
    Modified UNet with inverted residual block and depthwise seperable convolution
    """

    def __init__(self, class_num=3):
        super(MobileUNet, self).__init__()

        c = [16, 24, 32, 64, 96, 160, 320, 1280]

        # encoding arm
        self.conv3x3 = self.depthwise_conv(3, 32, p=1, s=2)
        self.irb_bottleneck1 = self.irb_bottleneck(32, 16, 1, 1, 1)
        self.irb_bottleneck2 = self.irb_bottleneck(16, 24, 2, 2, 6)
        self.irb_bottleneck3 = self.irb_bottleneck(24, 32, 2, 2, 6)
        self.irb_bottleneck4 = self.irb_bottleneck(32, 64, 3, 2, 6)
        self.irb_bottleneck5 = self.irb_bottleneck(64, 96, 3, 1, 6)
        self.irb_bottleneck6 = self.irb_bottleneck(96, 128, 3, 2, 6)
        self.irb_bottleneck7 = self.irb_bottleneck(128, 160, 1, 1, 6)

        self.conv1x1_encode = nn.Conv2d(160, 224, kernel_size=1, stride=1)

        # decoding arm
        self.D_irb1 = self.irb_bottleneck(224, 96, 1, 2, 6, True)
        self.D_irb2 = self.irb_bottleneck(96, 32, 1, 2, 6, True)
        self.D_irb3 = self.irb_bottleneck(32, 24, 1, 2, 6, True)
        self.D_irb4 = self.irb_bottleneck(24, 16, 1, 2, 6, True)
        self.DConv4x4 = nn.ConvTranspose2d(16, 16, 4, 2, 1, groups=16, bias=False)
        

        # Final layer: output channel number can be changed as per the usecase
        self.conv1x1_decode = nn.Conv2d(16, class_num, kernel_size=1, stride=1)

    def depthwise_conv(self, in_c, out_c, k=3, s=1, p=0):
        """
        optimized convolution by combining depthwise convolution and
        pointwise convolution.
        """
        conv = nn.Sequential(
            nn.Conv2d(in_c, in_c, kernel_size=k, padding=p, groups=in_c, stride=s),
            nn.BatchNorm2d(num_features=in_c),
            nn.ReLU6(inplace=True),
            nn.Conv2d(in_c, out_c, kernel_size=1),
        )
        return conv
    
    def irb_bottleneck(self, in_c, out_c, n, s, t, d=False):
        """
        create a series of inverted residual blocks.
        """
        convs = []
        xx = InvertedResidualBlock(in_c, out_c, s, t, deconvolve=d)
        convs.append(xx)
        if n>1:
            for i in range(1,n):
                xx = InvertedResidualBlock(out_c, out_c, 1, t, deconvolve=d)
                convs.append(xx)
        conv = nn.Sequential(*convs)
        return conv
    
    def get_count(self, model):
        # simple function to get the count of parameters in a model.
        num = sum(p.numel() for p in model.parameters() if p.requires_grad)
        return num
    
    def forward(self, x):
        # Left arm/ Encoding arm
        #D1
        x1 = self.conv3x3(x) #(32, 256, 256)
        x2 = self.irb_bottleneck1(x1) #(16,256,256) s1
        x3 = self.irb_bottleneck2(x2) #(24,128,128) s2
        x4 = self.irb_bottleneck3(x3) #(32,64,64) s3
        x5 = self.irb_bottleneck4(x4) #(64,32,32)
        x6 = self.irb_bottleneck5(x5) #(96,32,32) s4
        x7 = self.irb_bottleneck6(x6) #(160,16,16)
        x8 = self.irb_bottleneck7(x7) #(256,16,16)
        x9 = self.conv1x1_encode(x8) #(384,16,16) s5

        # Right arm / Decoding arm with skip connections
        d1 = self.D_irb1(x9) + x6   # (96,32,32) + (96,32,32) = (96, 32, 32)
        d2 = self.D_irb2(d1) + x4   # (32,64,64) + (32,64,64) = (32,64,64)
        d3 = self.D_irb3(d2) + x3   # (24,128,128) + (24,128,128) = (24,128,128)
        d4 = self.D_irb4(d3) + x2   # (16,256,256) + (16,256,256) = (16,256,256)
        d5 = self.DConv4x4(d4)      # (16,256,256) 
        # d5 = F.interpolate(d4, scale_factor=2, mode='bilinear', align_corners=True)
        
        out = self.conv1x1_decode(d5) # (3,512,512)

        return out


if __name__ == "__main__":
    print("[MobileUNet]")

    x = torch.rand((1, 3, 512, 512))

    model = MobileUNet()
    out = model(x)
    print(out.size())


    torch.save(model, "model.pth")
    torch.onnx.export(
        model,
        x,
        "model.onnx"
    )