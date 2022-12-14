import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from companies.serializers import CompanyGroupSerializer
from companies.utils import check_group_is_under_company, get_assigned_marketer_from_company_lead
from feedbacks.serializers import FeedbackSerializer
from leads.models import LeadContact
from users.serializers import UserDetailSerializer


class LeadContactUpdateCreateSerializer(serializers.ModelSerializer):
    """
    This is used to create leads
    """

    class Meta:
        model = LeadContact
        fields = [
            "id",
            "prefix",
            "groups",
            "last_name",
            "first_name",
            "email",
            "middle_name",
            "thumbnail",
            "job_title",
            "department",
            "sector",
            "want",
            "mobile",
            "lead_source",
            "assigned_marketer",
            "verified",
            "gender",
            "category",
            "timestamp",
        ]
        read_only_fields = ["id", "timestamp", ]

    def create(self, validated_data):
        # the groups are in this form groups=[<group instance>, ...] which are the instances
        # of a category
        global groups
        group_exists = validated_data.get("groups")
        if group_exists:
            # if the group was sent from the frontend I have to pop it out because i cant create
            # lead if it exists it would return an error
            groups = validated_data.pop('groups')
        instance = LeadContact.objects.create(**validated_data)
        ###########################################################
        """Add group if it exists on the data from the frontend"""
        if group_exists:
            for item in groups:
                # check if the user has access to using ths groups
                if not check_group_is_under_company(instance.company, item):
                    raise ValidationError("You dont have access to the groups provided")
                try:
                    instance.groups.add(item)
                except Exception as a:
                    print(a)
        ################################################################
        """ Assigned a marketer to the lead"""
        instance.assigned_marketer = get_assigned_marketer_from_company_lead(instance.company)
        instance.save()

        return instance


class LeadContactDetailSerializer(serializers.ModelSerializer):
    """
    This is meant to list all serializer for lead contact
    """
    groups = CompanyGroupSerializer(many=True)
    assigned_marketer = UserDetailSerializer(read_only=True)
    all_previous_feedbacks = serializers.SerializerMethodField(read_only=True)
    group_list = serializers.SerializerMethodField(read_only=True)
    assigned_marketer_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LeadContact
        fields = [
            "id",
            "prefix",
            "groups",
            "group_list",
            "last_name",
            "first_name",
            "middle_name",
            "thumbnail",
            "job_title",
            "department",
            "sector",
            "want",
            "email",
            "mobile",
            "lead_source",
            "assigned_marketer",
            "assigned_marketer_list",
            "all_previous_feedbacks",
            "verified",
            "gender",
            "category",
            "timestamp",
        ]

    def get_assigned_marketer_list(self, obj: LeadContact):
        """
        List of marketers currently on company .
        It won't show the admin or owner with in the list
        :param obj: LeadContact
        :return: marketer_list dictionary
        """
        try:
            marketer_info_list = obj.company.companyemployee_set.filter(
                role="MARKETER", status="ACTIVE").values_list(
                "user__id",
                "user__first_name",
                "user__last_name", )
            # Initialize a list for the user ids
            datasets = []
            for item in marketer_info_list:
                checked = False
                if not item[0]:
                    # sometimes it can be none
                    continue
                if item[0] == obj.assigned_marketer.id:
                    # If the marketer id is within then we know he is the current one
                    checked = True
                json_item = {
                    'id': str(item[0]),
                    'first_name': item[1],
                    'last_name': item[2],
                    'status': checked
                }
                datasets.append(json_item)
            return datasets
        except Exception as a:
            print(a)
            return None

    def get_group_list(self, obj: LeadContact):
        """
        List of groups in the db
        Return status if category selected in lead contact
        """
        try:
            datasets = []
            for c in obj.company.group_set.all():
                # Get all groups currently on this company
                if c in obj.groups.all():
                    checked = True  # Checked categories
                else:
                    checked = False
                json_item = {
                    'id': str(c.id),
                    'title': c.title,
                    'status': checked
                }
                # append the item to the list
                datasets.append(json_item)
            return datasets
        except Exception as a:
            print(a)
            return None

    def get_all_previous_feedbacks(self, instance):
        #  get the previous feedback
        feedback = instance.all_previous_feedbacks()
        if feedback:
            serializer = FeedbackSerializer(feedback, many=True)
            return serializer.data
        return None
