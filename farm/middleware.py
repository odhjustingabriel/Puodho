import logging
from datetime import timedelta

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.utils import timezone

security_logger = logging.getLogger('farm.security')


class RateLimitMiddleware:
    """Rate limiting with global, auth-IP, and auth-username lockouts."""

    ALL_LIMIT = 240
    AUTH_LIMIT = 5
    AUTH_USER_LIMIT = 5
    WINDOW_SECONDS = 15 * 60
    AUTH_PATH_PREFIXES = ('/accounts/login/', '/admin/login/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self._client_ip(request)
        path = request.path

        if self._is_limited(f'rl:all:{ip}', self.ALL_LIMIT):
            security_logger.warning('rate_limit_global ip=%s path=%s', ip, path)
            return self._too_many('Too many requests. Please try again later.')

        if path.startswith(self.AUTH_PATH_PREFIXES):
            if self._is_limited(f'rl:auth:ip:{ip}', self.AUTH_LIMIT):
                security_logger.warning('rate_limit_auth_ip ip=%s path=%s', ip, path)
                return self._too_many('Too many authentication attempts. Try again in 15 minutes.')

            username = self._submitted_username(request)
            if username and self._is_limited(f'rl:auth:user:{username.lower()}', self.AUTH_USER_LIMIT):
                security_logger.warning('rate_limit_auth_user user=%s ip=%s path=%s', username, ip, path)
                return self._too_many('Too many authentication attempts for this account. Try again in 15 minutes.')

        return self.get_response(request)

    def _is_limited(self, key, limit):
        added = cache.add(key, 1, timeout=self.WINDOW_SECONDS)
        if added:
            return False
        count = cache.get(key, 0) + 1
        cache.set(key, count, timeout=self.WINDOW_SECONDS)
        return count > limit

    @staticmethod
    def _submitted_username(request):
        if request.method != 'POST':
            return ''
        return (request.POST.get('username') or '').strip()[:150]

    @staticmethod
    def _client_ip(request):
        trusted = set(getattr(settings, 'TRUSTED_PROXY_IPS', []))
        remote_addr = request.META.get('REMOTE_ADDR', 'unknown')
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded_for and remote_addr in trusted:
            return forwarded_for.split(',')[0].strip()
        return remote_addr

    @staticmethod
    def _too_many(message):
        retry_at = timezone.now() + timedelta(minutes=15)
        return HttpResponse(f'{message} Retry after {retry_at:%H:%M}.', status=429)
