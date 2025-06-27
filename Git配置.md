# 下载
[官方网址](https://git-scm.com/downloads)下载安装包

# Visual Studio Code 配置

在 `Setting` 中搜索*git.path*，将路径 `root_path\Git\bin\git.exe` 写入setting.json文件

# 查看全部的全局配置

```
git config --global --list
```

# 配置代理服务器

可以解决的问题：vscode无法clone代码，因为无法连接外网。

访问Github.com需要配置代理服务器。

## （1）设置全局代理：
```
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```
其中端口可以到系统设置->网络和Internet->代理中查看。

## （2）取消全局代理
此外，如果不希望使用代理，可以运行下列命令：
```
git config --global --unset http.proxy 
git config --global --unset https.proxy
```

## （3）一次性设置代理
```
git config --global http.proxy 127.0.0.1:7890
git config --global https.proxy 127.0.0.1:7890
```

其中端口可以到系统设置->网络和Internet->代理中查看。

## （4）Git永久代理
你也可以通过设置环境变量来让Git使用代理，这通常在shell配置文件中设置，如.bashrc或.zshrc
```
export http_proxy=http://proxyuser:proxypwd@proxy.server.com:8080
export https_proxy=https://proxyuser:proxypwd@proxy.server.com:8080
```

# 用户名和邮箱配置

```
git config --global user.name "ZPJ-LEFT"
git config --global user.email 2724682324@qq.com
```
