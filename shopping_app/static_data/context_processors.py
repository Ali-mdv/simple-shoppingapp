from .models import SiteInfo


def site_info(request):
    try:
        info = SiteInfo.objects.get(status=True)
    except:
        info = None
    return {'site_info': info}
