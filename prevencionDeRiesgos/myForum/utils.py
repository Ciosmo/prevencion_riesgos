from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

def update_views(request, object):
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(object)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {"pk": hit_count.pk}
    hitCountResponse = HitCountMixin.hit_count(request, hit_count)
    
    if hitCountResponse.hit_counted:
        hits+=1
        hitcontext["hitcounted"] = hitCountResponse.hit_counted
        hitcontext["hit_message"] = hitCountResponse.hit_message
        hitcontext["tota_hits"] = hits