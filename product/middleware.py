from .models import IPAdrees

class IPAdressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            ip_address = IPAdrees.objects.get(ip_address=ip)
        except :
            ip_address = IPAdrees(ip_address=ip)
            ip_address.save()

        request.user.ip_address = ip_address

        response = self.get_response(request)

        return response