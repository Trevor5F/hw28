import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
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


# @method_decorator(csrf_exempt, name="dispatch")
# class UserCreateView(CreateView):
#     model = User
#     fields = ('first_name', 'last_name', 'username', 'password', 'role', 'age','location')
#
#     def post(self, request, *args, **kwargs):
#         user_data = json.loads(request.body)
#
#         new_user = User.objects.create(
#             first_name=user_data['first_name'],
#             last_name=user_data['last_name'],
#             username=user_data['username'],
#             password=user_data['password'],
#             role=user_data['role'],
#             age=user_data['age'],
#         )
#
#
#         return JsonResponse({
#             'id': new_user.id,
#             'first_name': new_user.first_name,
#             'last_name': new_user.last_name,
#             'username': new_user.username,
#             'role': new_user.role,
#             'age': new_user.age},
#             safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'username', 'password', 'role', 'age','location')

    def path(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.first_name = user_data['first_name'],
        self.object.last_name = user_data['last_name'],
        self.object.username = user_data['username'],
        self.object.password = user_data['password'],
        self.object.role = user_data['role'],
        self.object.age = user_data['age']

        self.object.save()


        return JsonResponse({
            'id': self.object.id,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'username': self.object.username,
            'role': self.object.role,
            'age': self.object.age},
            safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)