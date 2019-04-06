from rest_framework import serializers
from .models import Poll, Entry, Comment, Vote


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ('__all__')


class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('__all__')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('__all__')


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('__all__')
