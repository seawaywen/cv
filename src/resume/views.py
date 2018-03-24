from django.shortcuts import render # noqa 
from django.http import HttpResponse # noqa 
from django.utils.translation import ugettext_lazy as _  # noqa 
from django.utils import translation

from .models import WorkExperience, Project


def home(request):
    _work_experience = WorkExperience.objects.first()
    work_experience_trans_list = [] 
    if _work_experience:
        work_experience_trans_list = _work_experience.translations.all()

    keys_list = {'language': _('Language'), 'company': _('Company'),
                 'position': _('Job Position'), 'location': _('Location'),
                 'date_start': _('Start Date'), 'date_end': _('End Date'),
                 'contribution': _('Contribution'), 
                 'keywords': _('Keywords')
                }
                 
    work_experience_list = []

    current_lang = translation.get_language()
    for work_experience in work_experience_trans_list:
        if work_experience.language == current_lang:
            we1_fields = {}
            for _key, _value in keys_list.items():
                we1_fields[_value] = getattr(work_experience, _key)
            
            work_experience_list.append(we1_fields)
    
    include_list = {'title': _('Title'), 'download_link': _('Download Link'), 
                    'live_link': _('Live Link'), 'github': _('Github'), 
                    'description': _('Description')
                   }
    project_list = []
    for project in Project.objects.all():
        _fields = {}
        for _key, _value in include_list.items():
            _fields[_value] = getattr(project, _key)
        project_list.append(_fields)
    #print(project_list)

    context = {
        'work_experience_list': work_experience_list,
        'project_list': project_list
    }
    return render(request, 'resume/index.html', context)
