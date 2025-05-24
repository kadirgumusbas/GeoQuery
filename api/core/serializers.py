from rest_framework import serializers
from core.models import MembershipPlan, CustomUser, Membership, PastMembership, Query, Geo
from django.contrib.auth import get_user_model

User = get_user_model()


class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = '__all__'


class GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geo
        fields = '__all__'


class PastMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastMembership
        fields = '__all__'


class QuerySerializer(serializers.ModelSerializer):
    geo = GeoSerializer()

    class Meta:
        model = Query
        fields = '__all__'

    def create(self, validated_data):
        geo_data = validated_data.pop('geo')
        query = Query.objects.create(**validated_data)
        Geo.objects.create(query=query, **geo_data)
        return query


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    memberships = MembershipSerializer(many=True, read_only=True)
    past_memberships = PastMembershipSerializer(many=True, read_only=True)
    queries = QuerySerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'name', 'surname', 'phone', 'created',
            'memberships', 'past_memberships', 'queries'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'surname', 'email', 'password', 'confirmPassword', 'phone']

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        return User.objects.create_user(**validated_data)


class GeoWithQuerySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='query.user.username')
    membership_plan = serializers.CharField(source='query.membershipPlan.name')
    query_time = serializers.DateTimeField(source='query.queryTime')

    class Meta:
        model = Geo
        fields = ['lat', 'lng', 'username', 'membership_plan', 'query_time']


