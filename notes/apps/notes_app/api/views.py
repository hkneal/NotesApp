from rest_framework import generics, mixins
from apps.notes_app.models import Note, Label
from .serializers import NoteRUDSerializer, LabelRUDSerializer
from django.db.models import Q
#

class NotesApiView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field        = 'pk'
    serializer_class    = NoteRUDSerializer

    def get_queryset(self):
        return Note.objects.all()

    def perform_create(self, serializer):
        serializer.save(notes_list=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class LabelApiView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field        = 'pk'
    serializer_class    = LabelRUDSerializer

    def get_queryset(self):
        qs = Label.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(label__icontains=query)).distinct()
        # qs = Note.objects.filter(pk__in=qs)  Not working
        return qs

    def perform_create(self, serializer):
        serializer.save(notes_list=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class NotesApiRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field        = 'pk'
    serializer_class    = NoteRUDSerializer

    def get_queryset(self):
        return Note.objects.all()

class LabelApiRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field        = 'pk'
    serializer_class    = LabelRUDSerializer

    def get_queryset(self):
        return Label.objects.all()
