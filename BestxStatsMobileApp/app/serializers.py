from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password','first_name','last_name')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         # user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
#         user = User(username=validated_data['username'],email=validated_data['email'], first_name=validated_data['first_name'],last_name=validated_data['last_name'])
#         user.set_password(validated_data['password'])
#         user.save()
#         return user

class UserProfileSerializer(serializers.ModelSerializer):
    """
    A student serializer to return the student details
    """
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('user','device_type','device_token',)

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.set_password(password)
        user.save()
        profile, created = Profile.objects.update_or_create(user=user,
                            device_type=validated_data['device_type'],device_token=validated_data['device_token'])
        return profile