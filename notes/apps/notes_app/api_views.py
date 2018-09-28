from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .serializers import NoteSerializer
from .models import Note, Label
from .forms import SignupForm, LoginForm, CreateNoteForm, CreateLabelForm

#API Views

#POST a new URL
class CreateView(generics.CreateAPIView):
    #queryset = UrlName.objects.all()
    serializer_class = UrlNameSerializer

    def create(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"Fail": "Make sure a fully qualified URL is sent"})

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print serializer.data
        return Response({"Success": "Your shortened URL is: " + current_site.name + "/" + serializer.data['nick_name'] }, headers=headers)

    def perform_create(self, serilizer):
        serilizer.save()

#Get all URLs
class GetView(generics.ListAPIView):
    queryset = UrlName.objects.all()
    serializer_class = UrlNameSerializer

#Get full URL from a nick_name
class GetNickNameView(generics.ListAPIView):
    serializer_class = UrlNameSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        nick_name = self.kwargs['nick_name']
        queryset = self.model.objects.filter(nick_name = nick_name)
        return queryset
