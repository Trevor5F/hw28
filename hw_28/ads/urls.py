from django.urls import path

from ads.views import ads as ads_view, category as cat_view, users as users_view

urlpatterns = [
    path('', cat_view.CategoryListView.as_view()),
    path('<int:pk>', cat_view.CategoryDetailView.as_view()),
    path('create/', cat_view.CategoryCreateView.as_view()),
    path('<int:pk>/update/', cat_view.CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', cat_view.CategoryDeleteView.as_view()),

    # path('', ads_view.AdListView.as_view()),
    # path('<int:pk>', ads_view.AdDetailView.as_view()),
    # path('create/', ads_view.AdCreateView.as_view()),
    # path('<int:pk>/update/', ads_view.AdUpdateView.as_view()),
    # path('<int:pk>/delete/', ads_view.AdDeleteView.as_view()),
    # path('<int:pk>/upload_image/', ads_view.AdUploadImageView.as_view()),

    # path('', users_view.UserListView.as_view()),
    # path('<int:pk>', users_view.UserDetailView.as_view()),
    # path('create/', users_view.UserCreateView.as_view()),
    # path('<int:pk>/update/', users_view.UserUpdateView.as_view()),
    # path('<int:pk>/delete/', users_view.UserDeleteView.as_view()),
]