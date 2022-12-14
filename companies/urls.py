from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CompanyRetrieveUpdateDeleteAPIView, CompanyListCreateAPIView, CompanyModifyEmployeeAPIView, \
    CompanyGroupRetrieveUpdateDestroy, CompanyGroupListCreate, LocationViewSetsAPIView, IndustryViewSetsAPIView, \
    CompanyInviteListCreateAPIView, InvitedEmployeeSearchCompanyAPIView, CompanyEmployeesListAPIView, \
    CompanyLittleInfoListAPIView,CompanyAnalyTicsAPIView

urlpatterns = [
    path("", CompanyListCreateAPIView.as_view(), name="company_list_create"),
    path("company/<str:id>/", CompanyRetrieveUpdateDeleteAPIView.as_view(), name="company_ret_updt_delete"),
    path("company_action/<str:id>/", CompanyModifyEmployeeAPIView.as_view(), name="company_add_user"),
    # groups route
    path("groups/", CompanyGroupListCreate.as_view(), name="company_group_list_create"),
    path("groups/<str:group_id>/", CompanyGroupRetrieveUpdateDestroy.as_view(),
         name="company_group_create_retrieve_destroy"),
    path("company_invites/", CompanyInviteListCreateAPIView.as_view(), name="company_invites"),
    path("company_employees/", CompanyEmployeesListAPIView.as_view(), name="company_employees"),
    path("company_id_from_invite/", InvitedEmployeeSearchCompanyAPIView.as_view(), name="company_id_from_invite"),
    path("company_little_info/", CompanyLittleInfoListAPIView.as_view(), name="company_little_info"),
    path("company_analytics/", CompanyAnalyTicsAPIView.as_view(), name="company_analytics"),
]

router = DefaultRouter()
router.register(r'locations', LocationViewSetsAPIView, basename='locations')
router.register(r'industries', IndustryViewSetsAPIView, basename='industries')
urlpatterns += router.urls
