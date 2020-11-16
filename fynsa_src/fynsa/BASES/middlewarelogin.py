import re

from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
import pdb

EXEMPT_URL =[re.compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings,'LOGIN_EXEMPT_URLS'):
    EXEMPT_URL += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

#print('middleware EXEMPT URL : ', EXEMPT_URL)
#print('middleware LOGIN_URL : ', settings.LOGIN_URL)
class MiddlewareLogin:
    
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        response = self.get_response(request)
        return response

    def process_view(self,request,view_func,view_args,view_kargs):
        #pdb.set_trace()
        assert hasattr(request,'user')
        path = request.path_info.lstrip('/')
        url_is_exempt = any(url.match(path) for url in EXEMPT_URL)
        #print('**middleware** url_is_exempt: ',url_is_exempt)
        #print('**middleware** se está pidiendo path: ',path)
        #print('**middleware** autenticado: ',request.user.is_authenticated)
        
        

        if path == reverse('logout').lstrip('/'):
            logout(request)
        '''
        if request.user.is_authenticated and url_is_exempt:
            print('redirigido a la entrada via LOGIN REDIRECT URL')
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated or url_is_exempt:
            print('None')
            print('None **middleware** autenticado: ',request.user.is_authenticated)
            print('None **middleware** url_is_exempt: ',url_is_exempt)
            return None
        else:
            print('redirigido a la entrada via LOGIN_URL')
            return redirect(settings.LOGIN_REDIRECT_URL)
        '''

        # acá vamos a hacer otra forma

        if url_is_exempt:
            if request.user.is_authenticated:
                return None
            else:
                return None
        
        else:
            if request.user.is_authenticated:
                return None
            else:
                return redirect(settings.LOGIN_REDIRECT_URL)


  
        