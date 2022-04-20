import django_filters , floppyforms
from .models import TaskData






class TaskDataFilter(django_filters.FilterSet):
    task_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = TaskData
        fields = ['task_name']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(args)
        print(kwargs["queryset"])
        temp=kwargs["queryset"]
        # task_name_val = TaskData.objects.values_list('task_name')
        # print(task_name_val)
        
        TASK_NAME_CHOICES = []
        for i in temp:
            print(i)
            TASK_NAME_CHOICES.append(i.task_name)
        print(TASK_NAME_CHOICES)    
        self.filters['task_name'].extra.update({'widget': floppyforms.widgets.Input(datalist=TASK_NAME_CHOICES)})