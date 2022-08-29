import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import User, Location


class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.filter(ad__is_published=True).annotate(total_ads=Count('ad')).order_by('username')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)


        ads = []
        for user in page_obj:
            ads.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'role': user.role,
                'age': user.age,
                'location': list(map(str, user.location.all())),
                'total_ads': user.total_ads,
            })

        response = {
             "items": ads,
             "num_pages": page_obj.paginator.num_pages,
             "total": page_obj.paginator.count
         }

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except:
            return JsonResponse({"error": "Not found"}, status=404)


        return JsonResponse({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'location': list(map(str, user.location.all())),
            })


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ('first_name', 'last_name', 'username', 'password', 'role', 'age','location')

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        new_user = User.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role'],
            age=user_data['age'],
        )

        for location in user_data["locations"]:
            location_obj, created = Location.objects.get_or_create(name=location)
            new_user.location.add(location_obj)
        new_user.save()



        return JsonResponse({
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'username': new_user.username,
            'role': new_user.role,
            'age': new_user.age,
            'locations': list(map(str, new_user.location.all()))},
            safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'username', 'password', 'age','location')

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.first_name = user_data['first_name'],
        self.object.last_name = user_data['last_name'],
        self.object.username = user_data['username'],
        self.object.password = user_data['password'],
        self.object.age = user_data['age']

        for location in user_data["locations"]:
            try:
                location_obj = Location.objects.get(name=location)
            except Location.DoesNotExist:
                return JsonResponse({"error": "Location no found"}, status=404)
            self.object.location.add(location_obj)


        self.object.save()


        return JsonResponse({
            'id': self.object.id,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'username': self.object.username,
            'role': self.object.role,
            'age': self.object.age,
            "location": list(self.object.location.all().values_list("name", flat=True))},
            safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
