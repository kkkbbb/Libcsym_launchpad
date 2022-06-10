# Libcsym_launchpad
简易的libc-database，从launchpad下载符号包生成libc符号文本文件，直接用全局变量匹配libc版本如：unsorted泄漏main_arena；以及查看变量偏移，方便观察可控范围内的变量，如house of corrosion。

用法：

```
python3 get.py  #从launchapd下载符号
python3 find.py offset func/var   #偏移 函数名/变量
```

