from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from testimonials.models import Testimonial


# Create your views here.
def index(request):
    test_list = Testimonial.objects.all()
    paginator = Paginator(test_list, 20)

    page = request.GET.get('page')
    try:
        test_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        test_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        test_list = paginator.page(paginator.num_pages)

    return render(request, 'testimonials/index.html', {
        'test_list': test_list,
    })

def detail(request, test_id):
    testimonial = get_object_or_404(Testimonial, pk=test_id)
    return render(request, 'testimonials/detail.html', {
        'testimonial': testimonial,
    })