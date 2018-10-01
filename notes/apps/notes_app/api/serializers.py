from rest_framework import serializers
from apps.notes_app.models import Note, Label

class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['pk', 'title', 'note', 'created_at', 'updated_at', 'notes']
        read_only_fields = ['pk', 'notes', 'created_at', 'updated_at']

        def validate_title(self, title):
            if len(title) <= 0:
                raise serializers.ValidationError("This field is required and should be 45 charactes or less.")
            return title

        def validate_note(self, note):
            if len(note) <= 0 or len(note) > 500:
                raise serializers.ValidationError("This field is required and should be 500 charactes or less.")
            return note

class LabelSerializer(serializers.ModelSerializer):
    labels = NoteSerializer
    class Meta:
        model = Label
        fields = ['pk', 'created_at', 'label', 'labels']
        read_only_fields = ['pk', 'created_at', 'updated_at']
