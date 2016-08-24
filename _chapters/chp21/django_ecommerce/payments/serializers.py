from payments.models import User
from rest_framework import serializers
PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length


class PasswordSerializer(serializers.Serializer):
    """
    Reset password serializer
    """
    password = serializers.CharField(
        max_length=PASSWORD_MAX_LENGTH
    )
    password2 = serializers.CharField(
        max_length=PASSWORD_MAX_LENGTH,
    )

    def validate_password2(self, attrs, source):
        pwd2 = attrs[source]
        pwd = attrs['password']
        if pwd2 != pwd:
            raise serializers.ValidationError("Passwords don't match")

        return attrs

    def restore_object(self, attrs, instance=None):
        """ change password """
        if instance is not None:
            print("set password")
            instance.set_password(attrs.get('password'))
            return instance

        # we don't create new instances
        return None
