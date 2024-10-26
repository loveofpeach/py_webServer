from django.http import HttpResponse

class BlockedIPSMiddleware(object):
    def __init__( self, get_response ):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    '''中间件类'''
    EXCLUDE_IPS = ['127.0.0.1']

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        '''视图函数调用之前会调用'''
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in BlockedIPSMiddleware.EXCLUDE_IPS:
            return HttpResponse('<h1>Forbidden</h1>')

class TestMiddleware(object):
    '''中间件类'''
    def __init__( self, get_response ):
        print('---init---')
        self.get_response = get_response

    def __call__(self, request):
        '''产生 request 对象之后，url 匹配之前调用'''
        print('----process_request----')
        # return HttpResponse('process_request me')
        response=self.get_response(request)
        # 视图函数调用之后，内容返回浏览器之前
        print('------process-response------')
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        '''url 匹配之后，视图函数调用之前调用'''
        print('----process_view----')
        # view 视图函数没有得到执行，但是还是要走 process_response
        # return HttpResponse('process_view')

class ExceptionTest1Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        '''视图函数发生异常时调用'''
        print('----process_exception1----')
        print(exception)

class ExceptionTest2Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        '''视图函数发生异常时调用'''
        print('----process_exception2----')