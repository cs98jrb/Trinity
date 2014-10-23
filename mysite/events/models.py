from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    venue = models.ForeignKey(Venue)
    pub_date = models.DateTimeField('date published')
    
class Venue(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):              # __unicode__ on Python 2
        return self.choice_text
