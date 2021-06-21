from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import profile
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = ('phone',)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self, data):
        phone = data.get('phone')
        flag = bool(re.match('[\d]{10}', phone))

        if flag:
            if profile.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get('request'), phone=phone, password='a@for@apple')
            else:
                msg = {
                    'status': False,
                    'Message': 'Invalid Mobile number!!!',
                }
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'status': False,
                    'Message': 'Mobile number is incorrect!!!',
                }
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = {
                'status': False,
                'Message': 'Invalid Data Provided!!!',
            }
            raise serializers.ValidationError(msg, code='authorization')

        data['userData'] = user
        return data
