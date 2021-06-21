import re
from .otp import generate_otp, generate_username, update_otp, get_otp
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import profile
from .serializer import LoginSerializer
from django.contrib.auth import login as signin
from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView


class login(APIView):
    def post(self, request):
        mob = request.data.get('phone')
        if mob:
            flag = bool(re.match('[\d]{10}', mob))
        else:
            flag = False

        if flag:
            otp = generate_otp(mob)

            if otp == '-1':
                return Response({
                    'status': False,
                    'Message': 'Failed to send OTP',
                })

            try:
                obj = profile.objects.get(phone__iexact=mob)

                if obj.calls_left <= 0:
                    return Response({
                        'status': False,
                        'Message': 'Reached daily limit!!!',
                    })

                update_otp(mob, otp)
                obj.calls_left -= 1
                obj.save(update_fields=['calls_left', ])

                return Response({
                    'status': True,
                    'account_type': 'old',
                })
            except profile.DoesNotExist:

                update_otp(mob, otp)
                return Response({
                    'status': True,
                    'account_type': 'new',
                })

        else:
            return Response({
                'status': False,
                'Message': 'Invalid Mobile Number!!!'
            })


class verify_user(APIView):
    def post(self, request):
        mob = request.data.get('phone')
        otp = request.data.get('otp')

        if mob and otp:
            flag = bool(re.match('[\d]{10}', mob)) and bool(re.match('[\d]{6}', otp))
        else:
            flag = False

        if flag:
            try:
                obj = profile.objects.get(phone__iexact=mob)
                otpObj = get_otp(mob, otp)

                if not otpObj:
                    return Response({
                        'status': False,
                        'Message': 'Verification Unsuccessful!!!'
                    })

                return Response({
                    'status': True,
                    'Message': 'Verification Successful!!!',
                    'account_type': 'old',
                    'username': obj.username,
                })
            except profile.DoesNotExist:

                otpObj = get_otp(mob, otp)

                if not otpObj:
                    return Response({
                        'status': False,
                        'Message': 'Verification Unsuccessful!!!'
                    })
                username = generate_username()
                obj = profile.objects.create(phone=mob, username=username)
                obj.set_password('a@for@apple')
                obj.save()

                return Response({
                    'status': True,
                    'Message': 'Verification Successful!!!',
                    'account_type': 'new',
                    'username': username,
                })
        else:
            return Response({
                'status': False,
                'Message': 'Invalid Data!!!'
            })


class user_login(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request, format=None):
        mob = request.data.get('phone')

        if mob:
            flag = bool(re.match('[\d]{10}', mob))
        else:
            flag = False

        if flag:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['userData']
            signin(request, user)
            return super().post(request, format=None)
        else:
            return Response({
                'status': False,
                'Message': 'Invalid Data!!!'
            })
