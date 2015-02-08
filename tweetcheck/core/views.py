from django.core.mail import send_mail
from django.db import transaction, IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

import django_filters
import json

from .models import Organization, TweetCheckUser, Device, Action
from .permissions import IsOrganizationAdmin
from .serializers import UserSerializer, DeviceSerializer, ActionSerializer

class OrganizationQuerysetMixin(object):
    def get_queryset(self):
        if self.model.__name__ == 'Tweet':
            return self.model.objects.filter(handle__organization=self.request.user.organization)
        elif self.model.__name__ == 'Device':
            return self.model.objects.filter(user__organization=self.request.user.organization)
        else:
            return self.model.objects.filter(organization=self.request.user.organization)

class UserFilter(django_filters.FilterSet):
    token = django_filters.CharFilter(name='auth_token__key')

    class Meta:
        model = TweetCheckUser
        fields = ['is_approver', 'token']

class UserViewSet(OrganizationQuerysetMixin, viewsets.ModelViewSet):
    model = TweetCheckUser
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,IsOrganizationAdmin)
    filter_class = UserFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeviceViewSet(OrganizationQuerysetMixin, viewsets.ModelViewSet):
    model = Device
    serializer_class = DeviceSerializer
    filter_fields = ('token',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class ActionViewSet(OrganizationQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    model = Action
    serializer_class = ActionSerializer
    filter_fields = ('tweet',)
    paginate_by = 10

@require_http_methods(['POST'])
@csrf_exempt
def register(request):
    data = json.loads(request.body.decode('utf-8'))

    try:
        with transaction.atomic():
            organization = Organization.objects.create(name=data['organization'])
            user = TweetCheckUser.objects.create_user(
                email=data['email'],
                password=data['password'],
                organization=organization,
                is_active=False,
                is_approver=True)
    except IntegrityError:
        return JsonResponse(
            {'error': 'Email address {0} already has a TweetCheck account'.format(data['email'])},
            status=400
        )

    token = user.auth_token.key

    send_mail('Activate your TweetCheck account',
        'Click here to activate your account: http://www.tweetcheck.com/auth/activate?key={0}'.format(token),
        'no-reply@tweetcheck.com', [user.email], fail_silently=False)

    return HttpResponse()

def activate(request):
    token = request.GET['key']

    user = TweetCheckUser.objects.get(auth_token__key=token)

    if user.is_active:
        # This user is already active - no need to activate them
        return redirect('/')

    user.is_active = True
    user.save()

    new_token = user.replace_auth_token()

    return redirect('/activate?token={0}'.format(new_token.key))
