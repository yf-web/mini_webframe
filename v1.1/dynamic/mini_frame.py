import re

URL_FUNC_DICT = dict()


# 路由装饰器
def route(url):
    def set_func(func):
        URL_FUNC_DICT[url] = func

        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func


@route('/index.html')
def index():
    with open("./templates/index.html") as f:
        content = f.read()

    my_stock_info = "哈哈哈哈 这是你的本月名称....."

    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content
     

@route('/center.html')
def center():
    with open("./templates/center.html") as f:
        content = f.read()

    my_stock_info = "这里是从mysql查询出来的数据。。。"

    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content
     

def application(env, start_response):
    """
    wsgi接口
    :param env:
    :param start_response:
    :return:
    """
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    
    file_name = env['PATH_INFO']

    try:
        return URL_FUNC_DICT[file_name]()
    except Exception as e:
        return "Exception %s" % str(e)