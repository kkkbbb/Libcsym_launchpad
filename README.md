# Libcsym_launchpad
简易的libc database，从launchpad下载符号包提取符号信息，支持匹配全局变量，基本上可以匹配ubuntu绝大部分版本

用法：

```
python3 get.py  #从launchapd下载符号
python3 find.py offset func/var   #偏移 函数名/变量
```

