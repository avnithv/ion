# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import Group as DjangoGroup
from django.db import models
from django.db.models import Manager, Q

from .notifications import event_approval_request
from ..announcements.models import Announcement
from ..eighth.models import EighthScheduledActivity
from ..users.models import User
from ...utils.date import is_current_year, get_date_range_this_year
from ...utils.deletion import set_historical_user


class Link(models.Model):
    """A link about an item (Facebook event link, etc)."""
    url = models.URLField(max_length=2000)
    title = models.CharField(max_length=100)


class EventQuerySet(models.query.QuerySet):

    def this_year(self):
        """ Get Events from this school year only. """
        start_date, end_date = get_date_range_this_year()
        return self.filter(added__gte=start_date, added__lte=end_date)


class EventManager(Manager):

    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def visible_to_user(self, user):
        """Get a list of visible events for a given user (usually request.user).

        These visible events will be those that either have no groups
        assigned to them (and are therefore public) or those in which
        the user is a member.

        """

        return Event.objects.filter(approved=True).filter(Q(groups__in=user.groups.all()) | Q(groups__isnull=True) | Q(user=user))

    def hidden_events(self, user):
        """Get a list of events marked as hidden for a given user (usually request.user).

        These are all events visible to the user -- they have just decided to
        hide them.

        """
        ids = user.events_hidden.all().values_list("event__id")
        return Event.objects.filter(id__in=ids)


class EventUserMap(models.Model):
    """Represents mapping fields between events and users.

    These attributes would be a part of the Event model, but if they are,
    the last updated date is changed whenever a student sees or hides an event.

    Access these through event.user_map

    If you are checking to see whether a user has hidden an event, use:
        Event.objects.hidden_events(user)

    Attributes:
        event
            The one-to-one mapping between this object and the Event it is for
        users_hidden
            A many-to-many field of Users who have hidden this event

    """
    event = models.OneToOneField("Event", related_name="_user_map", on_delete=models.CASCADE)
    users_hidden = models.ManyToManyField(User, blank=True, related_name="events_hidden")

    def __str__(self):
        return "UserMap: {}".format(self.event.title)


class Event(models.Model):
    """An event available to the TJ community.

    title:
        The title for the event
    description:
        A description about the event
    links:
        Not currently used
    added:
        Time created (automatically set)
    updated:
        Time last modified (automatically set)
    time:
        The date and time of the event
    location:
        Where the event is located
    user:
        The user who created the event.
    scheduled_activity:
        An EighthScheduledActivity that should be linked with the event.
    announcement:
        An Announcement that should be linked with the event.
    groups:
        Groups that the event is visible to.
    attending:
        A ManyToManyField of User objects that are attending the event.
    show_attending:
        Boolean, whether users can mark if they are attending or not attending.
    show_on_dashboard:
        Boolean, whether the event will be shown on the dashboard.
    approved:
        Boolean, whether the event has been approved and will be displayed.
    approved_by:
        ForeignKey to User object, the user who approved the event.
    rejected:
        Boolean, whether the event was rejected and shouldn't be shown in the
        list of events that need to be approved.
    rejected_by:
        ForeignKey to User object, the user who rejected the event.
    public:
        Boolean, whether the event is public and can be shown on the login page
    category:
        The category of the event, used for ordering on the login page.
    open_to:
        Whether this event is open to parents, students, or both, shown on the login page.

    """
    objects = EventManager()

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    links = models.ManyToManyField("Link", blank=True)
    added = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    time = models.DateTimeField()
    location = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, on_delete=set_historical_user)

    scheduled_activity = models.ForeignKey(EighthScheduledActivity, null=True, blank=True, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, null=True, blank=True, related_name="event", on_delete=models.CASCADE)

    groups = models.ManyToManyField(DjangoGroup, blank=True)

    attending = models.ManyToManyField(User, blank=True, related_name="attending")
    show_attending = models.BooleanField(default=True)

    show_on_dashboard = models.BooleanField(default=True)

    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, null=True, related_name="approved_event", on_delete=set_historical_user)
    rejected_by = models.ForeignKey(User, null=True, related_name="rejected_event", on_delete=set_historical_user)

    public = models.BooleanField(default=True, verbose_name="Show on Login Page")

    category = models.CharField(max_length=6, choices=(("school", "In School"), ("sports", "Sports")), default="school")

    open_to = models.CharField(max_length=8, choices=(("everyone", "Everyone"), ("students", "Students"), ("parents", "Parents")), default="everyone")

    def show_fuzzy_date(self):
        """Return whether the event is in the next or previous 2 weeks.

        Determines whether to display the fuzzy date.

        """
        date = self.time.replace(tzinfo=None)
        if date <= datetime.now():
            diff = datetime.now() - date
            if diff.days >= 14:
                return False
        else:
            diff = date - datetime.now()
            if diff.days >= 14:
                return False

        return True

    def created_hook(self, request):
        """Run when an event is created."""
        if not request.user.has_admin_permission('events'):
            # Send approval email
            event_approval_request(request, self)

    @property
    def is_this_year(self):
        """Return whether the event was created after September 1st of this school year."""
        return is_current_year(self.added)

    @property
    def dashboard_type(self):
        return "event"

    @property
    def pinned(self):
        """ TODO: implement event pinning """
        return False

    @property
    def user_map(self):
        try:
            return self._user_map  # pylint: disable=E1101; Defined via a related_name in EventUserMap
        except EventUserMap.DoesNotExist:
            return EventUserMap.objects.create(event=self)

    def __str__(self):
        if not self.approved:
            return "UNAPPROVED - {} - {}".format(self.title, self.time)
        else:
            return "{} - {}".format(self.title, self.time)

    class Meta:
        ordering = ["time"]


class TJStarUUIDMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=40)
