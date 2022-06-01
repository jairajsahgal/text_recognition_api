from rest_framework import serializers
from .models import Account, User, Picture
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100,error_messages={"required":"Password not given!"})

    class Meta:
        model = Account
        fields = ['username','email','password']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['image']

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')

        if email and password:
            account = Account.objects.filter(email=email)
            if not account.exists():
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg,code='authorization')
            else:
                account=account[0]
                user = authenticate(request=self.context.get('request'),username=account.username,password=password)
                if not user:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password"')
            raise serializers.ValidationError(msg,code='authorization')
        
        attrs['user']=user
        return attrs
        