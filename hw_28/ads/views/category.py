import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category



class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("name")

        return JsonResponse(data=[
            {"id": cat.id,
             "name": cat.name,
            }
            for cat in self.object_list
        ], safe=False, json_dumps_params={'ensure_ascii': False})



class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": category.id,
            "name": category.name,},
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )



@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = ('name',)

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        new_category = Category.objects.create(
            name=category_data['name'])

        return JsonResponse({
            'id': new_category.id,
            'name': new_category.name},
             safe=False)



@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ('name',)

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data['name']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name':self.object.name},
             safe=False)



@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
        except:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({"status": "ok"}, status=200)
