from django.shortcuts import render # noqa 
from django.http import HttpResponse # noqa 
from django.utils.translation import ugettext_lazy as _  # noqa 

from .models import WorkExperience


def home(request):
    _work_experience = WorkExperience.objects.first()
    work_experience_trans_list = [] 
    if _work_experience:
        work_experience_trans_list = _work_experience.translations.all()

    keys_list = ['language', 'company', 'position', 'location',
                 'date_start', 'date_end',
                 'contribution', 'keywords'
                 ]
    work_experience_list = []

    for work_experience in work_experience_trans_list:
        we1_fields = {}
        for key in keys_list:
            we1_fields[key] = getattr(work_experience, key)
        work_experience_list.append(we1_fields)

    context = {
        'work_experience_list': work_experience_list,
    }
    return render(request, 'resume/index.html', context)
