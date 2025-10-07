from rest_framework import serializers


class AccountValidationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6, trim_whitespace=True)

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must be numeric.")
        return value


class AccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
