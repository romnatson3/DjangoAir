import logging
import requests
from django.shortcuts import redirect
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import login, get_user_model


User = get_user_model()


logger = logging.getLogger(__name__)


def get_google_callback_url(request):
    return request.build_absolute_uri('/oauth/google/callback/')


class GoogleLoginView(View):
    def get(self, request):
        auth_url = (
            f'https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
            f'&client_id={settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID}'
            f'&redirect_uri={get_google_callback_url(request)}'
            '&scope=openid email profile&access_type=offline&prompt=consent'
        )
        logger.info(f'Redirecting to {auth_url}')
        return redirect(auth_url)


class GoogleCallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        logger.info(f'Google code: {code}')
        if not code:
            return HttpResponse('No code provided', status=400)
        token_data = {
            'code': code,
            'client_id': settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID,
            'client_secret': settings.SOCIAL_AUTH_GOOGLE_SECRET,
            'redirect_uri': get_google_callback_url(request),
            'grant_type': 'authorization_code',
        }
        token_response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
        token_json = token_response.json()
        logger.info(f'Token response: {token_json}')
        access_token = token_json.get('access_token')
        token_type = token_json.get('token_type')
        if not access_token:
            return HttpResponse('Failed to obtain access token', status=400)
        user_info_response = requests.get(
            'https://openidconnect.googleapis.com/v1/userinfo',
            headers={'Authorization': f'{token_type} {access_token}'}
        )
        user_info = user_info_response.json()
        logger.info(f'User info: {user_info}')
        email = user_info.get('email')
        if not email:
            return HttpResponse('Email not available', status=400)
        username = user_info.get('name')
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(username=username, email=email)
        else:
            user = User.objects.get(email=email)
        login(request, user)
        return redirect('/')
