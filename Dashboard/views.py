from django.shortcuts import render

# Create your views here.
from Dashboard.models import Input


def homepage(request):
    if request.method == 'GET':
        all_input = Input.objects.filter(is_active=True)

        # input_json = {}
        #
        # for each_input in all_input:
        #     input_json[each_input.name] = each_input.file.path

        return render(request, 'html/video_chooser.html', {'all_input': all_input})


def violation(request):
    return render(request, 'html/violation_chooser.html')