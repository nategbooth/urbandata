from rest_framework import serializers
from django.contrib.auth import get_user_model


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name', 'company')

    def save(self):
        user = get_user_model()(email=self.validated_data['email'],
                                first_name=self.validated_data.get('first_name', ""),
                                last_name=self.validated_data.get('last_name', ""),
                                company=self.validated_data.get('company', ""),
                                )
        user.set_password(self.validated_data['password'])
        user.save()

