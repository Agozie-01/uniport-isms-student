from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

User = get_user_model()

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        """
        Validate email format and uniqueness.
        """
        try:
            validate_email(value)  # Validate email format
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        
        # Ensure email is unique (excluding the current instance when updating)
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_username(self, value):
        """
        Validate that the username is unique and doesn't contain special characters.
        """
        if not value.isalnum():
            raise serializers.ValidationError("Username must contain only letters and numbers.")
        if User.objects.filter(username=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Username is already in use.")
        return value

    def validate_first_name(self, value):
        """
        Validate first name (no numbers or special characters).
        """
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only letters.")
        return value

    def validate_last_name(self, value):
        """
        Validate last name (no numbers or special characters).
        """
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only letters.")
        return value

    def validate(self, data):
        """
        Validate that passwords match.
        """
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Create a new admin user with a hashed password and set is_staff to True.
        """
        validated_data.pop('confirm_password')  # Remove confirm_password from the data
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.is_staff = True  # Set is_staff to True, making the user an admin
        user.save()  # Save the user with the updated is_staff value
        return user

    def update(self, instance, validated_data):
        """
        Update an existing admin user.
        """
        validated_data.pop('confirm_password', None)  # Remove confirm_password from the data
        password = validated_data.pop('password', None)

        # Apply field-level validations for each field
        instance = self.apply_field_validations(instance, validated_data)

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def apply_field_validations(self, instance, validated_data):
        """
        Run field-level validations and apply them for each field.
        """
        for field, value in validated_data.items():
            validate_method = getattr(self, f'validate_{field}', None)
            if validate_method:
                value = validate_method(value)
                validated_data[field] = value
        return instance
