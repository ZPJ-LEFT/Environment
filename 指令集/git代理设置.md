# Git一次性设置代理
```
git config --global http.proxy 127.0.0.1:7890
git config --global https.proxy 127.0.0.1:7890
```

其中端口可以到系统设置->网络和Internet->代理中查看。

# 取消代理
```
git config --global --unset http.proxy
git config --global --unset https.proxy
```

# Git永久代理
你也可以通过设置环境变量来让Git使用代理，这通常在shell配置文件中设置，如.bashrc或.zshrc
```
export http_proxy=http://proxyuser:proxypwd@proxy.server.com:8080
export https_proxy=https://proxyuser:proxypwd@proxy.server.com:8080
```
