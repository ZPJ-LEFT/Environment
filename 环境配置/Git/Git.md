# 下载
[官方网址](https://git-scm.com/downloads)下载安装包

# Visual Studio Code 配置

在 `Setting` 中搜索*git.path*，将路径 `root_path\Git\bin\git.exe` 写入setting.json文件

# 关于代理服务器

访问Github.com需要配置代理服务器。

设置全局代理：
```
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```
其中端口可以到系统设置->网络和Internet->代理中查看。

此外，如果不希望使用代理，可以运行下列命令：
```
git config --global --unset http.proxy 
git config --global --unset https.proxy
```
