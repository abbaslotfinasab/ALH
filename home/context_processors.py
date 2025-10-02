from .models import Availability

def availability_status(request):
    availability = Availability.objects.last()
    return {'availability': availability}
