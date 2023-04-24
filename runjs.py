import os
import json
import subprocess

'''
    代替 execjs 执行 js，为了指定编码而写
'''


class RunJs:
    def __init__(self, path: str = None, content: str = None, encoding: str = 'utf-8', back_status: bool = False):
        """

        :param path: js 路径
        :param content: js
        :param encoding: 编码格式
        :param back_status: 是否返回执行状态
        """
        self._path = path
        self._encoding = encoding
        self._back_status = back_status

        # 检查文件是否存在
        if self._path is not None:
            if not os.path.exists(self._path):
                raise FileNotFoundError(f'文件不存在：{self._path}')
            else:
                with open(path, 'r', encoding=self._encoding) as f:
                    self._content = f.read()
        else:
            self._content = content

        if self._path is None and self._content is None:
            raise NotImplementedError('请输入 js 路径或者 js 内容！')

    def run(self, *args, timeout: int = 5):
        """

        :param args: 输入参数
        :param timeout: 执行最大时间
        :return:
        """
        # 构造执行函数
        if len(args) == 1:
            return_str = '''
                    %s()
                ''' % args[0]
        else:
            return_str = '''
                    %s.apply(this, %s)
                ''' % (args[0], list(args)[1:])

        # 构造新函数
        new_content = '''
                (function(){
                    const runJsProcess = process;
                    %s
                    console.log('nodeBack over!'); // 存在的意义就是下面换行用
                    runJsProcess.stdout.write(JSON.stringify({nodeBack:%s}));
                })()
            ''' % (self._content, return_str)

        # 执行新函数
        p = subprocess.Popen(['node'], stdin=-1, stdout=-1, stderr=-1, universal_newlines=True, encoding=self._encoding)
        stdout, stderr = p.communicate(input=new_content, timeout=timeout)
        ret = p.wait()

        # 判断返回
        if ret != 0:
            if self._back_status:
                return {'status': False, 'result': stderr}
            return stderr

        if self._back_status:
            return {'status': True, 'result': json.loads(stdout.split('\n')[-1])['nodeBack']}
        return json.loads(stdout.split('\n')[-1])['nodeBack']


if __name__ == '__main__':
    # run_js = RunJs(path='test.js')
    run_js = RunJs(content='''
        function getCookie(){
            return arguments
        }
    ''')
    result = run_js.run('getCookie', 'Gk')
    print(result)
