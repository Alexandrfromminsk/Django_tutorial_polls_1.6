from django.db import models
from django.utils import timezone
import datetime

class Poll(models.Model):
    question = models.CharField(max_length=120)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return timezone.now() - datetime.timedelta(days=2) <= self.pub_date < now
    #for admin look
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Poll)
    answer = models.CharField(max_length=30)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.answer
