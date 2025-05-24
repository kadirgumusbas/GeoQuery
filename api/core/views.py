from xmlrpc.client import DateTime

from rest_framework.viewsets import ModelViewSet

from core import models
from django.db.models import Sum
from core.models import (
    MembershipPlan, CustomUser, Membership, PastMembership, Query, Geo, QuerySum
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from core.serializers import (
    MembershipPlanSerializer, UserSerializer, UserDetailSerializer,
    MembershipSerializer, PastMembershipSerializer,
    QuerySerializer, GeoSerializer, RegisterSerializer, GeoWithQuerySerializer
)
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.utils import timezone


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer


class MembershipPlanViewSet(ModelViewSet):
    permission_classes = [AllowAny]  # 🔓 Giriş serbest
    queryset = MembershipPlan.objects.all().order_by('price')
    serializer_class = MembershipPlanSerializer


class MembershipViewSet(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class PastMembershipViewSet(ModelViewSet):
    queryset = PastMembership.objects.all()
    serializer_class = PastMembershipSerializer


class QueryViewSet(ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer


class GeoViewSet(ModelViewSet):
    queryset = Geo.objects.all()
    serializer_class = GeoSerializer


def get_active_membership(user):
    now = timezone.now()

    # Aktif bir üyeliği var mı
    active = user.memberships.filter(membershipEnd__gt=now).order_by('-membershipStart').first()
    if active:
        return active

    # Aktif üyeliği yoksa: FREE planı ata
    free_plan = MembershipPlan.objects.filter(name__iexact='FREE').first()
    if free_plan:
        new_membership = Membership.objects.create(
            user=user,
            membershipPlan=free_plan,
            queryHour=free_plan.membershipQueryHour,
            queryDay=free_plan.membershipQueryDay
        )
        return new_membership

    return None


class UserGeoQueryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        geo_data = Geo.objects.filter(query__user=request.user).order_by('-query__queryTime')
        serializer = GeoWithQuerySerializer(geo_data, many=True)
        return Response(serializer.data)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # 🔓 Giriş serbest

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Giriş başarılı',
                'username': user.username,
                'token': token.key
            }, status=200)

        return Response({'error': 'Geçersiz kullanıcı adı veya şifre'}, status=400)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]  # 🔓 Giriş serbest

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                free_plan = MembershipPlan.objects.get(name='FREE')
            except MembershipPlan.DoesNotExist:
                return Response({'error': 'FREE planı bulunamadı.'}, status=500)

                #  Kullanıcıya membership oluştur
            Membership.objects.create(
                user=user,
                membershipPlan=free_plan,
                queryHour=free_plan.membershipQueryHour,
                queryDay=free_plan.membershipQueryDay
            )
            Token.objects.create(user=user)
            return Response({'message': 'Kayıt başarılı', 'username': user.username}, status=201)
        return Response(serializer.errors, status=400)


def create_query_for_user(user, lat, lng):
    membership = user.memberships.last()  # aktif üyelik

    # 🔄 Sorgu hakkı kontrolü
    membership.reset_query_limits_if_needed()

    if membership.queryHour <= 0 or membership.queryDay <= 0:
        raise PermissionError("Sorgu hakkınız kalmadı.")

    # Hakkı azalt
    membership.queryHour -= 1
    membership.queryDay -= 1
    membership.save()

    #  Query ve Geo kaydet
    query = Query.objects.create(user=user, membershipPlan=membership.membershipPlan)
    Geo.objects.create(query=query, lat=lat, lng=lng)

    #  QuerySum güncelle
    current_month = datetime(now().year, now().month, 1).date()
    summary, created = QuerySum.objects.get_or_create(user=user, month=current_month)
    summary.count += 1
    summary.save()

    return query


class QuerySearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        lat = request.data.get('lat')
        lng = request.data.get('lng')

        if not lat or not lng:
            return Response({'error': 'Koordinatlar eksik'}, status=400)

        try:
            query = create_query_for_user(request.user, float(lat), float(lng))
            return Response({
                'message': 'Sorgu başarıyla kaydedildi',
                'query_id': query.id,
                'timestamp': query.queryTime
            }, status=201)
        except PermissionError as e:
            return Response({'error': str(e)}, status=403)
        except Exception as e:
            return Response({'error': f'Bir hata oluştu: {str(e)}'}, status=500)


class MonthlyQueryStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        year = now().year

        # Tüm QuerySum kayıtlarını getir
        query_sums = QuerySum.objects.filter(user=user, month__year=year)

        # 12 aylık boş template oluştur
        data = []
        for month in range(1, 13):
            count = 0
            match = query_sums.filter(month__month=month).first()
            if match:
                count = match.count
            data.append({
                'month': datetime(year, month, 1).strftime('%b').upper(),  # 'JAN', 'FEB'...
                'count': count
            })

        return Response(data)


class MonthlyQueryStatsManagerAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        year = now().year
        query_sums = QuerySum.objects.filter(month__year=year)

        data = []
        for month in range(1, 13):
            month_total = query_sums.filter(month__month=month).aggregate(total=Sum('count'))['total'] or 0
            data.append({
                'month': datetime(year, month, 1).strftime('%b').upper(),
                'count': month_total
            })

        return Response(data)


class UserStatsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        year = now().year
        users = CustomUser.objects.all()
        query_sums = QuerySum.objects.filter(month__year=year)

        data = []
        for user in users:
            total_queries = query_sums.filter(user=user).aggregate(total=Sum('count'))['total'] or 0
            last_membership = None
            if hasattr(user, 'memberships'):
                last_membership = user.memberships.last()

            membership_name = getattr(
                getattr(last_membership, 'membershipPlan', None), 'name', 'YOK'
            )
            data.append({
                'username': user.username,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
                'phone': user.phone,
                'membership': membership_name,
                'totalQueries': total_queries
            })
        return Response(data)


class AdminUserGeoQueriesAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'detail': 'username parametresi gerekli.'}, status=400)

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Kullanıcı bulunamadı.'}, status=404)

        geo_data = Geo.objects.filter(query__user=user).order_by('-query__queryTime')
        serializer = GeoWithQuerySerializer(geo_data, many=True)
        return Response(serializer.data)


class RegisterPlanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        plan_id = request.data.get('planId')

        if not plan_id:
            return Response({'error': 'Plan ID gerekli.'}, status=400)

        try:
            plan = MembershipPlan.objects.get(id=plan_id)
        except MembershipPlan.DoesNotExist:
            return Response({'error': 'Plan bulunamadı.'}, status=404)

        # Eski aktif üyeliği pasife alma (isteğe bağlı)
        user.memberships.filter(membershipEnd__isnull=True).update(membershipEnd=timezone.now())

        # Yeni üyelik oluştur
        Membership.objects.create(
            user=user,
            membershipPlan=plan,
            queryHour=plan.membershipQueryHour,
            queryDay=plan.membershipQueryDay,
            membershipStart=timezone.now()
        )

        return Response({'message': f"{plan.name} planına başarıyla abone olundu."}, status=201)


class ProfilePlanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        membership = user.memberships.order_by('-membershipStart').first()

        plan_name = getattr(
            getattr(membership, 'membershipPlan', None),
            'name',
            'FREE'
        )

        return Response({'planName': plan_name})


class UserIsAdmin(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "is_admin": True,
        })

class AdminUserMonthlyAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        year = timezone.now().year
        users = CustomUser.objects.filter(date_joined__year=year)

        data = []
        for month in range(1, 13):
            count = users.filter(date_joined__month=month).count()
            data.append({
                'month': datetime(year, month, 1).strftime('%b').upper(),
                'count': count
            })

        return Response(data)
