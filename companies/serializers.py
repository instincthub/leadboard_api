from rest_framework import serializers

from users.serializers import UserDetailSerializer
from .models import Company, Group, Industry, Location


class IndustrySerializer(serializers.ModelSerializer):
    """
    this is used to list the industry , create, update
    """

    class Meta:
        model = Industry
        fields = [
            "id",
            "name",
            "timestamp",
        ]

        read_only_fields = ["id", "timestamp", ]


class LocationSerializer(serializers.ModelSerializer):
    """
    this is used to create location , list location and update the location
    """

    class Meta:
        model = Location
        fields = [
            "id",
            "state",
            "country",
            "timestamp",
        ]
        read_only_fields = ["id", "timestamp", ]


class CompanyCreateUpdateSerializer(serializers.ModelSerializer):
    """
    This is used to create a company  .
    """
    industry = IndustrySerializer()

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "website",
            "phone",
            "industry",
            "overview",
            "company_size",
            "headquater",
            "founded",
            "locations",
            "timestamp",
        ]
        read_only_fields = ["id", "timestamp", ]

    def create(self, validated_data):
        # the locations are in this form locations=[<locations instance>, ...] which are the instances
        # of a category
        locations = validated_data.pop('locations')
        instance = Company.objects.create(**validated_data)
        for item in locations:
            try:
                instance.locations.add(item)
            except Exception as a:
                print(a)
        return instance


class CompanySerializer(serializers.ModelSerializer):
    """
    This is used to list all  company's or get the detail .
    """
    owner = UserDetailSerializer(read_only=True)
    admins = UserDetailSerializer(many=True)
    marketers = UserDetailSerializer(many=True)
    locations = LocationSerializer(many=True)
    industry = IndustrySerializer()

    class Meta:
        model = Company
        fields = [
            "id",
            "owner",
            "name",
            "website",
            "phone",
            "industry",
            "overview",
            "company_size",
            "headquater",
            "founded",
            "locations",
            "admins",
            "marketers",
            "timestamp",
        ]
        read_only_fields = ["id", "timestamp", ]


class CompanyAddUserSerializer(serializers.Serializer):
    """
    This is meant to add user to the company
    """
    company_user_type = serializers.ChoiceField(choices=[("ADMIN", "ADMIN"), ("MARKETER", "MARKETER")])
    action = serializers.ChoiceField(choices=[("ADD", "ADD"), ("DELETE", "DELETE"), ])
    email = serializers.EmailField()


class CompanyGroupSerializer(serializers.ModelSerializer):
    """
    This serializer is meant to create a group under a company
    """

    class Meta:
        model = Group
        fields = [
            "id",
            "title",
            "slug",
            "timestamp",
        ]
        read_only_fields = ["id", "timestamp", "slug"]


class CompanyRequestSerializer(serializers.Serializer):
    """
    This serializer is meant to send request to the admin about joining the company
    """
    company_id = serializers.UUIDField()
    message = serializers.CharField(max_length=10000)


class OwnerAddUserSerializer(serializers.Serializer):
    """
    This serializer is meant to be used to add user to an organisation or company
    """
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=(("MARKETER", "MARKETER"),
                 ("ADMIN", "ADMIN"),)
    )
    action = serializers.ChoiceField(
        choices=(
            ("ADD", "ADD"),
            ("REMOVE", "REMOVE"),
        )
    )
    company_id = serializers.UUIDField()
