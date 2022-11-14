from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from companies.models import Company
from companies.utils import check_admin_access_company
from users.permissions import NotLoggedInPermission, IsAuthenticatedOrReadOnly
from .models import Job, JobSchedule, Applicant
from .serializers import JobCreateUpdateSerializer, JobListDetailSerializer, JobScheduleSerializer, ApplicantSerializer


class JobListCreateAPIView(ListCreateAPIView):
    """create a job post needs you to be authenticated and also be the owner or admin of the company"""
    permission_classes = [NotLoggedInPermission]
    serializer_class = JobListDetailSerializer
    queryset = Job.objects.all()

    def get_company(self, *args, **kwargs):
        # the company id
        company_id = self.request.query_params.get("company_id")
        #  this filter base on the company id  provided
        if not company_id:
            return None
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return None
        return company

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = JobListDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = JobListDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # get the company we need
        company = self.get_company()
        job_type = self.request.query_params.get("job_type")
        if company and job_type:
            # if the company exists and also the job_type was passed
            return self.filter_queryset(self.queryset.filter(company=company, job_type__icontains=job_type))
        if company:
            return self.filter_queryset(self.queryset.filter(company=company))
        return self.filter_queryset(self.queryset)

    def create(self, request, *args, **kwargs):
        if not self.get_company():
            return Response({"error": "Company id required on params"}, status=400)
        if not self.request.user.is_authenticated:
            return Response({"error": "You are currently not authenticated"}, status=400)
        if not check_admin_access_company(self.request.user, self.get_company()):
            return Response({"error": "You dont have permission to create a job under the company "}, status=401)
        serializer = JobCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=self.get_company())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class JobRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = JobListDetailSerializer
    permission_classes = [NotLoggedInPermission]
    queryset = Job.objects.all()
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.request.user.is_authenticated:
            return Response({"error": "You are currently not authenticated"}, status=401)
        if not check_admin_access_company(self.request.user, instance.company):
            return Response({"error": "You dont have permission to create a job under the company "}, status=401)
        serializer = JobCreateUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.request.user.is_authenticated:
            return Response({"error": "You are currently not authenticated"}, status=401)
        if not check_admin_access_company(self.request.user, instance.company):
            return Response({"error": "You dont have permission to delete a job under the company "}, status=401)
        # Fixme: right now i am deleting all the applicants
        instance.applicants.all().delete()
        instance.delete()
        return Response(status=204)


class JobScheduleViewSetsAPIView(ModelViewSet):
    """this viewset enables the full crud which are create, retrieve,update and delete  """
    serializer_class = JobScheduleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = JobSchedule.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # I only override this just to add partial true
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class JobApplyAPIView(CreateAPIView):
    """
    this view enables users to apply to a job post.
    it requires the id of the job post the user is applying to
    """
    serializer_class = ApplicantSerializer
    permission_classes = [NotLoggedInPermission]

    def get_job(self):
        """
        the job_id needs to be passed in the params and if it wasn't the user wont be added to the job applicants,
        but it just raises a 404 page
        :return:
        """
        job_id = self.request.query_params.get("job_id")
        if not job_id:
            raise Http404
        job = Job.objects.filter(id=job_id).first()
        if not job:
            raise Http404
        return job

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.get_job().applicants.filter(email=serializer.validated_data.get("email")).exists():
            return Response(status=400, data={"error": "Already applied to this job post."})
        serializer.save()
        # Get the applicant which was saved
        applicant = Applicant.objects.filter(id=serializer.data.get("id")).first()
        if not applicant:
            return Response(status=404, data={"error": "Applicant not saved"})
        job = self.get_job()
        job.applicants.add(applicant)
        return Response({"message": "Successfully applied to this job"}, status=200)