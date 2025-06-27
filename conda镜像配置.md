# conda install 加速

## 配置清华源

清华大学开源软件镜像站 ：https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```

## 删除添加的源，恢复官方源

```
conda config --remove-key channels
conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
```

## 查看源的优先权，比如

```
conda config --get channels
conda config --show channels
```

下面的是输出
```
--add channels 'defaults'   # lowest priority
--add channels 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/'
--add channels 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/'   # highest priority
```
