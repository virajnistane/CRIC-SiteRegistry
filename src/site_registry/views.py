from django.http import JsonResponse # type: ignore
from django.views import View # type: ignore


class WelcomeView(View):
    """Simple welcome page showing available endpoints"""
    
    def get(self, request):
        return JsonResponse({
            'message': 'Welcome to CRIC (Computing Resource Information Catalogue) API',
            'version': '0.1.0',
            'endpoints': {
                'admin': '/admin/',
                'api_root': '/api/',
                'sites_list': '/api/sites/',
                'site_detail': '/api/sites/{id}/',
            },
            'docs': {
                'development': '/docs/DEVELOPMENT.md',
                'testing': '/docs/TESTING.md',
            }
        })
