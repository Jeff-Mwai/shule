from rest_framework import serializers

from SchoolApp.models import User, Assignment, Fee


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ['user_permissions', 'groups']


    def create(self, validated_data):
        password = validated_data.get('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ['file','description','current_class']

    def create(self, validate_data):
        user = User.object.filter(id=2).first()
        assignment = Assignment(**validate_data)
        assignment.user = user
        assignment.save()

        return  assignment

class FeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fee
        exclude = ['user']

    def create(self, validate_data):
        user = User.object.filter(id=2).first()
        fee = Fee(**validate_data)
        fee.user = user
        fee.save()

        return fee
