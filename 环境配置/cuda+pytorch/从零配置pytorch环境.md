# 配置cuda+pytorch

## 0.版本对应关系

需要安装并确认以下内容的版本，以下包含一个可行的示例版本：
- python=3.8
- nvidia显卡驱动=515.76 （CUDA Version:11.7）
- CUDA=11.7
- pytorch=2.0.0 (包含cuDNN)

## 1.安装Anaconda

(1) 创建虚拟环境

```
conda create -n name python=3.8
```

(2) 激活虚拟环境

```
activate name
```

(3) 删除虚拟环境

```
conda remove -n xxxxx(名字) --all
```

## 2. 安装pip

```
conda install pip
```

## 3. 安装CUDA

先确定显卡驱动版本，以及其能支持的CUDA的最大版本，如果指令报错，先去安装显卡驱动：
```
nvidia-smi
```

随后安装对应版本的CUDA

## 4. 安装cuDNN（似乎pytorch自带cuDNN，可跳过）

## 5. 安装Pytorch

在pytorch官网上查询对应CUDA版本的torch安装指令，例如，基于CUDA 11.7的torch=2.0.0安装命令：

```
pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1
```

## 6. 安装完成确认

进入python界面，输入：

```
import torch
torch.cuda.is_available()
```

输出True则安装完成
