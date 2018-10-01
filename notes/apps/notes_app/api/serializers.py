from rest_framework import serializers
from apps.notes_app.models import Note, Label

class NoteRUDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['pk', 'title', 'note', 'created_at', 'updated_at', 'notes_list']
        read_only_fields = ['pk', 'notes_list', 'created_at', 'updated_at']

        def validate_title(self, title):
            if len(title) <= 0:
                raise serializers.ValidationError("This field is required and should be 45 charactes or less.")
            return title

        def validate_note(self, note):
            if len(note) <= 0 or len(note) > 500:
                raise serializers.ValidationError("This field is required and should be 500 charactes or less.")
            return note

class LabelRUDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ['pk', 'created_at', 'label', 'labels_list']
        read_only_fields = ['pk', 'labels_list', 'created_at', 'updated_at']
