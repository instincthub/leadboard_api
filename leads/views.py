from django.http import Http404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from companies.models import Company
from companies.utils import check_marketer_and_admin_access_company, check_company_high_value_content_access
from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackCreateSerializer
from users.permissions import LoggedInPermission, NotLoggedInPermission
from users.utils import date_filter_queryset
from .models import LeadContact
from .serializers import LeadContactUpdateCreateSerializer, LeadContactDetailSerializer


class LeadContactCreateListAPIView(ListCreateAPIView):
    """
    This class is meant to list all the lead contact and also create a new one
    """
    permission_classes = [NotLoggedInPermission]
    serializer_class = LeadContactDetailSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "last_name",
        "first_name",
        "middle_name",
        "job_title",
        "sector",
        "lead_source",
        "want",
    ]

    def get_company(self):
        #  filter the company base on the id provided
        company_id = self.request.query_params.get("company_id")
        company = Company.objects.filter(id=company_id).first()
        if not company:
            raise Http404
        return company

    def get_queryset(self):
        """
        this filter using the company id passed on the urls to get the leads associated with it
        :return:
        """
        queryset = self.filter_queryset(self.get_company().leadcontact_set.all())
        if queryset:
            # Filter the date if it is passed in the params like
            # ?from_date=2222-12-12&to_date=2223-11-11 or the word ?seven_days=true or ...
            # You will get more from the documentation
            queryset = date_filter_queryset(request=self.request, queryset=queryset)
        return queryset

    def create(self, request, *args, **kwargs):
        #  before creating a lead we have to make sure the user is a member of that company
        company = self.get_company()
        serializer = LeadContactUpdateCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Getting the email and checking if an email exists on this leads under the company
        email = serializer.validated_data.get("email")
        lead_contact_email_exists = LeadContact.objects.filter(email=email, company=company).first()
        if lead_contact_email_exists:
            # The lead email must be unique under an organisation
            return Response({"error": "Lead with that email already exists under this organisation"}, status=400)

        high_value_content = serializer.validated_data.get("high_value_content")
        #  if the high value content id exists from the validated data that means the user want
        #  the lead just to download ebook or something else though
        if high_value_content:
            #  using the company which enables us to verify the high value content if it exists on the leads
            #  because some leads are meant just only to download ebooks .
            if not check_company_high_value_content_access(high_value_content, company):
                return Response({"error": "You dont have access to create this lead under this company ."}, status=401)
        if request.user.is_authenticated:
            #  first check for then company owner then the company admins or  the assigned marketer
            if not check_marketer_and_admin_access_company(self.request.user, company):
                return Response({"error": "You dont have permission"}, status=401)
            # if the user is logged in I save the lead with the user
            serializer.save(staff=self.request.user, company=company, high_value_content=high_value_content)
        else:
            serializer.save(company=company, high_value_content=high_value_content)
        return Response(serializer.data, status=201)


class LeadContactRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    this is used to update the lead , delete i, and also retrieve the lead .
    Note that once the lead is deleted the feedback connected ti will be deleted
    """
    permission_classes = [LoggedInPermission]
    serializer_class = LeadContactUpdateCreateSerializer
    lookup_field = "id"

    def get_object(self):
        # using the id of the company to filter through the leads
        company_id = self.request.query_params.get("company_id")
        # the lead id on the url
        id = self.kwargs.get("id")
        company = Company.objects.filter(id=company_id).first()
        if not company:
            raise Http404
        # get the lead base on the id of the company on the urls
        lead = company.leadcontact_set.filter(id=id).first()
        if not lead:
            raise Http404
        return lead

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        #  first check for then company owner then the company admins or  the assigned marketer
        if not check_marketer_and_admin_access_company(self.request.user, instance.company):
            return Response({"error": "You dont have permission"}, status=401)
        serializer = LeadContactDetailSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        #  first check for then company owner then the company admins or  the assigned marketer
        if not check_marketer_and_admin_access_company(self.request.user, instance.company):
            return Response({"error": "You dont have permission"}, status=401)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        ################################################################
        """                 Feedback create                 """
        #  now with the feedback data was
        #  passed also if available when updating the lead we need to create a feedback
        feedback_serializer = FeedbackCreateSerializer(data=request.data)
        #  check if the feedback serializer is valid and if it would not raise an exception
        if feedback_serializer.is_valid(raise_exception=False):
            feedback_content = feedback_serializer.validated_data.get("feedback_content")
            feedback_action = feedback_serializer.validated_data.get("feedback_action")
            feedback_next_schedule = feedback_serializer.validated_data.get("feedback_next_schedule")
            #  create the feedback with the helper function provided
            feedback = Feedback.objects.create_by_model_type(
                model_type="leadcontact",
                other_model_id=instance.id,
                feedback=feedback_content,
                action=feedback_action,
                next_schedule=feedback_next_schedule,
                staff=self.request.user
            )
        """End Feedback create"""
        ################################################################

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        #  first check for then company owner then the company admins or  the assigned marketer
        if not check_marketer_and_admin_access_company(self.request.user, instance.company):
            return Response({"error": "You dont have permission"}, status=401)
        self.perform_destroy(instance)
        return Response(status=204)
