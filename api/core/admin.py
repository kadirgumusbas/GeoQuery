from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import MembershipPlan, Query, Membership, PastMembership, Geo, CustomUser, QuerySum


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'name', 'surname', 'email', 'phone']
    readonly_fields = ['created']
    model = CustomUser

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'membershipQueryHour', 'membershipQueryDay']
    model = MembershipPlan

class GeoInline(admin.StackedInline):
    model = Geo
    can_delete = False
    extra = 0

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ['user', 'membershipPlan', 'queryTime']
    fields = ['user', 'membershipPlan', 'queryTime']
    inlines = [GeoInline]
    readonly_fields = ['queryTime']
    model = Query
    ordering = ('-queryTime',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'membershipPlan', 'membershipStart', 'membershipEnd', 'queryHour', 'queryDay']
    readonly_fields = ['membershipStart']
    model = Membership

@admin.register(PastMembership)
class PostMembershipAdmin(admin.ModelAdmin):
    list_display = ['membershipPlan', 'membershipStart', 'membershipEnd', 'membershipDay', 'querySum']
    readonly_fields = ['membershipStart', 'membershipEnd']
    model = PastMembership

@admin.register(QuerySum)
class QuerySumAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'count')


