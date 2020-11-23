from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'cpf', 'password',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False
            }
        }

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        cpf = validated_data['cpf']

        user = User.objects.create_user(email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.cpf = cpf
        user.save()

        return user
