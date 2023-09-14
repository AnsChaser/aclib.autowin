
import inspect, functools

def findfunc(func):

    """
    这是一个装饰器，用来装饰'Window'对象的目标查找方法，以便对其参数进行预处理，
    被装饰的方法名称要以'dm'或者'cv'开头，且带有形参'areas'和'lpoutput'，
    其参数将进行以下预处理：
        1. 断言查找函数的运行环境是否设置
        2. 将传入的单个区域转化为区域列表，并将空的区域默认设置为运行时窗口大小
        3. 自动设置lpoutput的内容，被装饰函数不需要再操作lpoutput
    """

    @functools.wraps(func)
    def wrappedfunc(self, *args, **kwargs):
        uselib = func.__name__[:2]
        ready = getattr(self, f'_{uselib}ready')
        assert ready, f'{uselib} not set'
        arguments = inspect.getcallargs(func, self, *args, **kwargs)
        areas = arguments['areas']
        lpoutput = arguments['lpoutput']
        if not areas or isinstance(areas[0], int):
            areas = [areas]
        arguments['areas'] = [area or (0, 0, *self.clientsize) for area in areas]
        found = func(**arguments)
        if isinstance(lpoutput, list):
            lpoutput.clear()
            lpoutput.extend(found if isinstance(found, list) else [found])
        return found
    return wrappedfunc
