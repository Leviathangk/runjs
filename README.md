# 介绍

调用 node 执行 js ，可指定编码格式

# 安装

```
pip install -U gexecjs
```

# 示例

```
    # run_js = RunJs(filepath='test.js')
    run_js = RunJs(content='''
        function getCookie(){
            return arguments
        }
    ''')
    result = run_js.run('getCookie', 'Gk')
    print(result)
```