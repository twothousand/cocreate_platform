from django.http import JsonResponse

from apps.dim.models import get_model, get_industry, get_ai_tag


def model_view(request):
    model = get_model().order_by('id')
    return JsonResponse({'model': list(model)}, safe=False)


def industry_view(request):
    industry = get_industry().order_by('id')
    return JsonResponse({'industry': list(industry)}, safe=False)


def ai_tag_view(request):
    ai_tag = get_ai_tag().order_by('id')
    return JsonResponse({'ai_tag': list(ai_tag)}, safe=False)
