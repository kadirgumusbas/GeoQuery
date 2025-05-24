"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    UserViewSet, MembershipPlanViewSet, MembershipViewSet,
    PastMembershipViewSet, QueryViewSet, GeoViewSet, RegisterAPIView, LoginAPIView, QuerySearchAPIView,
    MonthlyQueryStatsAPIView, UserGeoQueryView, MonthlyQueryStatsManagerAPIView, UserStatsAPIView,
    AdminUserGeoQueriesAPIView, RegisterPlanAPIView, ProfilePlanAPIView, UserIsAdmin, AdminUserMonthlyAPIView

)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'membership-plans', MembershipPlanViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'past-memberships', PastMembershipViewSet)
router.register(r'queries', QueryViewSet)
router.register(r'geos', GeoViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('query/', QuerySearchAPIView.as_view(), name='query-search'),
    path('monthly-stats/', MonthlyQueryStatsAPIView.as_view(), name='monthly-stats'),
    path('admin-monthly-stats/', MonthlyQueryStatsManagerAPIView.as_view(), name='admin-monthly-stats'),
    path('past-query/', UserGeoQueryView.as_view(), name='past-query'),
    path('admin-user-stats/', UserStatsAPIView.as_view(), name='admin-user-stats'),
    path('userGeo/', AdminUserGeoQueriesAPIView.as_view(), name='userGeo'),
    path('register-plan/', RegisterPlanAPIView.as_view()),
    path('user-plan/', ProfilePlanAPIView.as_view()),
    path('is-admin/',UserIsAdmin.as_view()),
    path('admin-monthly-users/',AdminUserMonthlyAPIView.as_view()),

]

urlpatterns += router.urls
