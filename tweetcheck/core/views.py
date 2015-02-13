from django.db import transaction, IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

import django_filters
import json

from .forms import RegisterForm, InviteForm, InvitedUserForm
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
    form = RegisterForm(json.loads(request.body.decode('utf-8')))

    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    try:
        with transaction.atomic():
            organization = Organization.objects.create(name=form.cleaned_data['organization'])
            user = TweetCheckUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                organization=organization,
                is_active=False,
                is_approver=True)
    except IntegrityError:
        return JsonResponse(
            {'error': 'Email address {0} already has a TweetCheck account.'.format(form.cleaned_data['email'])},
            status=400
        )

    user.send_activation_email()

    return HttpResponse()

@require_http_methods(['POST'])
@csrf_exempt
def invite(request):
    form = InviteForm(json.loads(request.body.decode('utf-8')))

    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    request_user = TweetCheckUser.objects.get(auth_token__key=request.META['HTTP_AUTHORIZATION'].split()[1])
    organization = request_user.organization

    try:
        user = TweetCheckUser.objects.create_user(
            email=form.cleaned_data['email'],
            password=get_random_string(), # Set a random password until the user is activated
            organization=organization,
            is_active=False,
            is_approver=form.cleaned_data['is_approver'])
    except IntegrityError:
        return JsonResponse(
            {'error': 'Email address {0} already has a TweetCheck account.'.format(form.cleaned_data['email'])},
            status=400
        )

    user.send_invitation_email()

    serializer = UserSerializer(user)

    return JsonResponse(serializer.data)

def reinvite_user(request):
    user_id = request.GET['user']

    try:
        user = TweetCheckUser.objects.get(pk=user_id)
    except TweetCheckUser.DoesNotExist:
        return JsonResponse(
            {'error': 'There was an error reinviting this user.'},
            status=400
        )

    if user.is_active:
        # The user is already active and doesn't need to be reinvited
        return HttpResponse()

    user.replace_auth_token()
    user.send_invitation_email()

    return HttpResponse()

@require_http_methods(['POST'])
@csrf_exempt
def activate_invitation(request):
    form = InvitedUserForm(json.loads(request.body.decode('utf-8')))

    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    try:
        user = TweetCheckUser.objects.get(auth_token__key=form.cleaned_data['token'])
    except TweetCheckUser.DoesNotExist:
        return JsonResponse(
            {'error': 'This invitation link is not valid. Please ask someone to invite you again.'},
            status=400
        )

    user.set_password(form.cleaned_data['password'])
    user.is_active = True
    user.save()

    new_token = user.replace_auth_token()

    return JsonResponse({'token': new_token.key})

def activate(request):
    token = request.GET['key']

    try:
        user = TweetCheckUser.objects.get(auth_token__key=token)
    except TweetCheckUser.DoesNotExist:
        return JsonResponse(
            {'error': 'This activation link is not valid. Have you registered this email address before?'},
            status=400
        )

    user.is_active = True
    user.save()

    new_token = user.replace_auth_token()

    return redirect('/activate?token={0}'.format(new_token.key))
