from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Poll, Entry, Comment, Vote
from account.models import User
from .serializers import PollSerializer, EntrySerializer, CommentSerializer, VoteSerializer
from .utils import httpResponse, httpResponseBadRequest, httpResponseNotFound
import json


class AllPolls(APIView):

    def get(self, request, user_id):
        if user_id == "visitor":
            all_polls = list(Poll.objects.all().values())
            for poll in all_polls:
                entries = list(Entry.objects.filter(
                    poll__id=poll["id"]).values())
                poll["entries"] = entries
            return httpResponse(all_polls)
        try:
            user = User.objects.get(id=user_id)
        except:
            return httpResponseNotFound('User not found.')
        all_polls = list(Poll.objects.all().values())
        for poll in all_polls:
            entries = list(Entry.objects.filter(poll__id=poll["id"]).values())
            poll["entries"] = entries
            if Vote.objects.filter(entry__poll__id=poll["id"], user=user).count() > 0:
                poll["has_voted"] = True
            else:
                poll["has_voted"] = False
        return httpResponse(all_polls)


class MyPolls(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        if user_id == None or user_id == "":
            return httpResponseBadRequest('Required fields missing.')
        my_polls = list(Poll.objects.filter(creater__id=user_id).values())
        for poll in my_polls:
            entries = list(Entry.objects.filter(poll__id=poll["id"]).values())
            poll["entries"] = entries
        return httpResponse(my_polls)


class PollDetail(APIView):

    def get(self, request, poll_id, user_id):
        try:
            poll = Poll.objects.get(id=poll_id)
        except:
            return httpResponseNotFound('Poll not found.')
        user = None
        if user_id != "visitor":
            try:
                user = User.objects.get(id=user_id)
            except:
                return httpResponseNotFound('User not found.')
        poll_serializer = PollSerializer(poll)
        returned = poll_serializer.data
        entries = []
        for entry in Entry.objects.filter(poll__id=poll_id):
            entry_serializer = EntrySerializer(entry)
            entries.append(entry_serializer.data)
        returned["entries"] = entries
        returned["voters"] = []
        all_votes = Vote.objects.filter(entry__poll__id=poll_id)
        for vote in all_votes:
            if not any(d['user_id'] == vote.user.id for d in returned["voters"]):
                returned["voters"].append(
                    {'user_id': vote.user.id, 'name': vote.user.name})
        if Vote.objects.filter(entry__poll__id=poll_id, user=user).count() > 0 or user_id == "visitor":
            returned["can_vote"] = False
        else:
            returned["can_vote"] = True
        return httpResponse(returned)


class PollEdit(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user_id = request.data["userId"]
            title = request.data["title"]
            description = request.data["description"]
            closedate = request.data["closedate"]
            allowed_votes = request.data["allowedVotes"]
            entries = request.data["entries"]
            for entry in entries:
                name = entry["name"]
        except:
            return httpResponseBadRequest('Required fields missing.')

        if "id" in request.data.keys():
            try:
                poll = Poll.objects.get(id=request.data["id"])
                poll.title = title
                poll.description = description
                poll.closedate = closedate
                poll.allowed_votes = allowed_votes
            except:
                return httpResponseNotFound('Poll not found.')
        else:
            try:
                user = User.objects.get(id=user_id)
            except:
                return httpResponseNotFound('User not found.')
            poll = Poll(title=title, description=description, creater=user,
                        closedate=closedate, allowed_votes=allowed_votes)
        poll.save()
        poll_serializer = PollSerializer(poll)
        data = poll_serializer.data

        entries_data = []
        entries_id = []
        for entry in entries:
            if "id" in entry.keys():
                entry_obj = Entry.objects.get(id=entry["id"])
                entry_obj.name = entry["name"]
            else:
                entry_obj = Entry(name=entry["name"], poll=poll)
            entry_obj.save()
            entries_id.append(entry_obj.id)
            entry_serializer = EntrySerializer(entry_obj)
            entries_data.append(entry_serializer.data)

        for entry in Entry.objects.filter(poll=poll):
            if entry.id not in entries_id:
                entry.delete()
        data["entries"] = entries_data
        return httpResponse(data)


class PollComments(APIView):

    def get(self, request, pollId):
        comments = list(Comment.objects.filter(
            entry__poll__id=pollId).values())
        for comment in comments:
            user_id = comment.pop("user_id")
            try:
                user = User.objects.get(id=user_id)
            except:
                return httpResponseBadRequest("User not found")
            comment["user"] = {"id": user.id, "name": user.name}
        return httpResponse(comments)


class CommentDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        comments = request.data
        returned = []
        for comment in comments:
            try:
                ts = comment["ts"]
                user_id = comment["userId"]
                content = comment["content"]
                entry_id = comment["entryId"]
            except:
                return httpResponseBadRequest('Required fields missing.')
            try:
                user = User.objects.get(id=user_id)
            except:
                return httpResponseNotFound('User not found.')
            try:
                entry = Entry.objects.get(id=entry_id)
            except:
                return httpResponseNotFound('Entry not found.')
            if 'replyto' in comment.keys():
                replytoId = comment["replyto"]
                replyto = Comment.objects.get(id=replytoId)
                comment = Comment(ts=ts, user=user,
                                  content=content, entry=entry, replyto=replyto)
            else:
                comment = Comment(ts=ts, user=user,
                                  content=content, entry=entry)

            comment.save()
            comment_serializer = CommentSerializer(comment)
            comment_data = comment_serializer.data
            comment_data["user"] = {
                "id": user.id, "name": user.name}
            returned.append(comment_data)

        return httpResponse(returned)


class PollVotes(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        returned = []
        try:
            user_id = request.data["userId"]
            ts = request.data["ts"]
            votes = request.data["votes"]
        except:
            return httpResponseBadRequest('Required fields missing.')
        try:
            user = User.objects.get(id=user_id)
        except:
            return httpResponseNotFound('User not found')
        for vote in votes:
            try:
                entryId = vote["entryId"]
            except:
                return httpResponseBadRequest('Required fields missing.')
            try:
                entry = Entry.objects.get(id=entryId)
            except:
                return httpResponseNotFound("Entry not found")
            entry.votes = entry.votes + 1
            entry.save()

            count = Vote.objects.filter(entry=entry, user=user).count()
            if count > 0:
                return httpResponseBadRequest('User has already voted.')
            vote = Vote(entry=entry, user=user, ts=ts)
            vote.save()
            vote_serializer = VoteSerializer(vote)
            returned.append(vote_serializer.data)
        return httpResponse(returned)


class LikeDetail(APIView):

    def post(self, request):
        try:
            comment_id = request.data["commentId"]
            liked = request.data["liked"]
        except:
            return httpResponseBadRequest('Required fields missing.')
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return httpResponseNotFound('Comment not found')
        if liked:
            comment.likes = comment.likes + 1
        else:
            comment.likes = comment.likes - 1
            if comment.likes < 0:
                comment.likes = 0
        comment.save()
        comment_serializer = CommentSerializer(comment)
        return httpResponse(comment_serializer.data)
