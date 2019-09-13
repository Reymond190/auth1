from django.shortcuts import render
from django.views.generic import ListView
from vehicles.models import vehicle
from app_auth.models import AddDevice


class search_listview(ListView):
    queryset = vehicle.objects.all()
    template_name = 'main/class.html'
    model = vehicle


    def get_queryset(self,*args,**kwargs):
        object_list = self.model.objects.all()
        return object_list

def searchlistview(request,*args,**kwargs):
    q = request.GET.get('q')
    print(q)
    if q is not None:
        queryset =vehicle.objects.filter(name__icontains=q)
    else:
        queryset = vehicle.objects.all()
    context = {
        'object_list' : queryset
    }
    return render(request,"search/view.html",context)



