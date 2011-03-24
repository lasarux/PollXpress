from django.db import models
from django.core.mail import EmailMessage
from django.template import loader, Context
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template import Template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import messages
import uuid
import datetime

# TODO: do it i18n friendly
# Query + Option = Closed question

class Query(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(_("Question"), max_length=30)
    description = models.TextField(_("Description")) # help
    date_creation = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return "%s (%i)" % (self.name, len(self.option_set.all()))
        
    def generate_ballots(self, request=None, space=False, date_finish=datetime.datetime.now()+datetime.timedelta(1)): # default is one day
        """This function generates valid ballots for a votation"""
        options = Option.objects.filter(query=self)
        bad_emails = []
        if not options or not space:
            return False # query with no options
        current_site = Site.objects.get_current().domain
        
        # create a poll
        if Poll.objects.filter(space=space, query=self):
            return False
        poll = Poll(query=self, space=space, date_finish=date_finish)
        poll.save()            
            
        # check for persons in that space
        persons = Person.objects.filter(space=space)
        if not persons:
            return False

        # create results for this poll
        results = []
        for option in options:            
            result = Result(poll=poll, option=option)
            result.save()
            results.append(result)
        
        # create ballots and send them
        for i in persons:
            ballots = []
            for result in results:
                uid = uuid.uuid4().hex
                b = Ballot(uid=uid, result=result, person=i)
                b.save()
                ballots.append(b)
                
            # prepare message
            t = loader.get_template('ballot_email.txt')
            c = Context({'person': i, 'poll': poll, 'ballots': ballots,
                         'current_site': current_site})
            message = t.render(c)
            try:
                i.send(_('PollXpress: %s') % poll.query.name, message)
                # mark ballots as sent
                for ballot in ballots:
                    ballot.sent = True
                    ballot.save()
            except:
                # to sent a warning mail to admin
                bad_emails.append(i)
                
        # send a list with bad emails to admin
        t = loader.get_template('ballot_bad_emails.txt')
        c = Context({'persons': bad_emails, 'space': space, 'name': self.name})
        message = t.render(c)
        email = EmailMessage(_('PollXpress: %s - emails with problems') % poll.query.name, 
            message, 'pollxpress@partidopirata.es', [space.admin.email])
        email.send()
        return True
        
    @models.permalink
    def get_absolute_url(self):
        return ('query-view', [str(self.id)])
        

# TODO: better statistics (gender, region, age...)

class Option(models.Model):
    query = models.ForeignKey(Query)
    name = models.TextField(_("Option"))
    description = models.TextField(_("Description")) # help
    
    def __unicode__(self):
        return "%s@%s" % (self.name, self.query.name)
    

# Space + Person = Groups of persons

class Space(models.Model):
    admin = models.ForeignKey(User) # TODO: add "friends" for cooperation
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('space-edit', [str(self.id)])

    
class Person(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    date = models.DateTimeField(default=datetime.datetime.now)
    space = models.ManyToManyField(Space, null=True, blank=True) # user could "live" with no space
    
    def send(self, subject, message):
        email = EmailMessage(subject, message, 'pollxpress@partidopirata.es', [self.email])
        email.send()

    def __unicode__(self):
        return "%s <%s>" % (self.name, self.email)


class Poll(models.Model):
    query = models.ForeignKey(Query)
    space = models.ForeignKey(Space, verbose_name=_("Space"))
    date_published = models.DateTimeField(default=datetime.datetime.now)
    date_finish = models.DateTimeField(blank=True, null=True)
    closed = models.BooleanField(_("Closed"), default=False)
    
    def __unicode__(self):
        return "%s@%s - %s" % (self.query, self.space, self.date_published.strftime("%d/%M/Y %H:%M"))
    
    # Currently reset isn't more an option (ballots have been deleted)
    def reset(self): 
        pass
    
    def get_result(self):
        results = self.result_set.all()
        total_ballots = float(sum([i.votes for i in results]))
        data = []
        for i in results:
            try:
                porcentage = ((i.votes/total_ballots)*100)
            except:
                porcentage = 0
            data.append({
                'option': i.option, 
                'votes': i.votes, 
                'porcentage': "%.2f" % porcentage
            })
        return data
        
    def get_votes_pending(self):
        total_options = len(self.query.option_set.all())
        return len(self.ballot_set.all())/total_options
    
    class Meta:
        unique_together = ("query", "space")

class Result(models.Model):
    poll = models.ForeignKey(Poll)
    option = models.ForeignKey(Option)
    votes = models.IntegerField(default=0)
    
    def __unicode__(self):
        return "%s@%s=%i" % (self.option.name, self.poll.query.name, self.votes)

# ballot: personalized items to perform a poll

class Ballot(models.Model):
    uid = models.CharField(max_length=256) # email in uid
    done = models.BooleanField(default=False) # FIXME: this isn't necessary already
    sent = models.BooleanField(default=False)
    result = models.ForeignKey(Result)
    person = models.ForeignKey(Person)
    
    def countit(self):
        # check if this ballot has been used and poll is active
        if not self.done and datetime.datetime.now()<=self.result.poll.date_finish:
            # count it
            self.result.votes += 1 # add 1 vote to this option
            self.result.save()
            self.send_confirmation()
            # delete person's ballots
            ballots = Ballot.objects.filter(result__poll=self.result.poll, person=self.person).delete()
            return True
        else:
            return False
        
    def send_confirmation(self):
        # prepare message
        t = loader.get_template('ballot_confirmation_email.txt')
        c = Context({'person': self.person, 'result': self.result})
        message = t.render(c)
        self.person.send(_('PollXpress: %s - Vote confirmation') % self.result.poll.query.name, message)


    def __unicode__(self):
        return "%s: %s@%s" % (self.uid, self.result.option.name, self.result.poll.query.name)

    @models.permalink
    def get_absolute_url(self):
        return ('vote', [self.uid])
