from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class MembershipPlan(models.Model):
    name = models.CharField(max_length=40)
    price = models.FloatField()
    membershipQueryHour = models.IntegerField(default=1)
    membershipQueryDay = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Membership(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='memberships')
    membershipPlan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE, related_name='active_memberships')
    membershipStart = models.DateTimeField(auto_now_add=True)
    membershipEnd = models.DateTimeField(null=True, blank=True)
    queryHour = models.IntegerField(default=0)
    queryDay = models.IntegerField(default=0)
    last_hour_reset = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_day_reset = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:  # sadece ilk oluşturulurken çalışır
            now = timezone.now()
            if self.membershipPlan.name.upper() == 'FREE':
                self.membershipEnd = now + timedelta(days=3650)  # 10 yıl
            else:
                self.membershipEnd = now + timedelta(days=30)  # 1 ay
            self.queryHour = self.membershipPlan.membershipQueryHour
            self.queryDay = self.membershipPlan.membershipQueryDay
        super().save(*args, **kwargs)

    def reset_query_limits_if_needed(self):
        now = timezone.now()

        # Saatlik sıfırlama
        if (now - self.last_hour_reset).total_seconds() >= 3600:
            self.queryHour = self.membershipPlan.membershipQueryHour
            self.last_hour_reset = now

        # Günlük sıfırlama
        if now.date() != self.last_day_reset.date():
            self.queryDay = self.membershipPlan.membershipQueryDay
            self.last_day_reset = now

        self.save()

    def __str__(self):
        return f"{self.queryDay} - {self.queryHour}"


class PastMembership(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='past_memberships')
    membershipPlan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE, related_name='past_memberships')
    membershipStart = models.DateTimeField(null=True, blank=True)
    membershipEnd = models.DateTimeField(null=True, blank=True)
    membershipDay = models.IntegerField(default=0)
    querySum = models.IntegerField(default=0)


class Query(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='queries')
    membershipPlan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE, related_name='queries')
    queryTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.membershipPlan.name} - {self.queryTime.strftime('%Y-%m-%d %H:%M:%S')}"


class Geo(models.Model):
    query = models.OneToOneField(Query, on_delete=models.CASCADE, related_name='geo')
    lat = models.FloatField()
    lng = models.FloatField()


class QuerySum(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    month = models.DateField()  # Yalnızca ay bilgisi yeterli (örn. 2025-05-01)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'month')
