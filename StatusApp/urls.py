from django.urls import path, include

from . import views

app_name = "status"
urlpatterns = [
    path("", views.GroupListView.as_view(), name="group_list"),
    path("group/", views.GroupListView.as_view(), name="sb-default"),
    path("group/add/", views.CreateGroup, name="sb-group-create"),
    path("group/<slug:slug>/", views.GroupMembersList, name="sb-group-view"),
    path(
        "group/<slug:slug>/mod/<slug:user>/<str:action>",
        views.GroupCRUD,
        name="sb-group-crud",
    ),
    path("group/<slug:slug>/mod", views.GroupModView, name="sb-group-mod"),
    path("group/<slug:slug>/user/search", views.UserSearch, name="user-search"),
    path("user/search/", views.UserStatusSearch, name="user-status-search"),
    path("userstatus/modal/<slug:slug>", views.UserStatusModal, name="user-modal"),
    path("members/<slug:slug>/", views.LoadGroupMembers, name="sb-group-members"),
]
