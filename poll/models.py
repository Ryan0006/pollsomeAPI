from django.db import models
from account.models import User


class Poll(models.Model):
    title = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=200, default="")
    closedate = models.CharField(max_length=30, default="")
    allowed_votes = models.IntegerField(default=1)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Entry(models.Model):
    name = models.CharField(max_length=50, default="")
    votes = models.IntegerField(default=0)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(models.Model):
    ts = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, default="")
    likes = models.IntegerField(default=0)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    replyto = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.user, self.entry)


class Vote(models.Model):
    ts = models.IntegerField(default=0)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.user, self.entry)
