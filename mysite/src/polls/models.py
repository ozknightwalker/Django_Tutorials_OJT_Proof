import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=255, blank=False, null=False)
    published = models.DateTimeField('Date Published')
    def __str__(self):
        return self.text
    def published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published <= now

    published_recently.admin_order_field = 'pub_date'
    published_recently.boolean=True
    published_recently.short_description = 'Published recently?'
    list_filter = ['published']
    search_fields = ['text']

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=255, blank=False, null=False)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
