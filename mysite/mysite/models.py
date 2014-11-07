from django.db import models

# Create your models here.

class EmailInf(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    sent_date = models.DateTimeField('date published',auto_now_add=True)
    
    class Meta:
        ordering = ['sent_date']
        
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name + ", (" +str(self.sent_date)+")"