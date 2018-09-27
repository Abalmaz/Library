from django.contrib.auth.models import AbstractUser
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from .abs_models import Timestamp
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.core.mail import send_mail
from django.template.loader import render_to_string
from mptt.models import MPTTModel, TreeForeignKey
import uuid


class Country(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class PublishingHouse(Timestamp):
    name = models.CharField(max_length=35)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Author(Timestamp):
    first_name = models.CharField(max_length=25)
    second_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, blank=True)
    pseudonym = models.CharField(max_length=25, blank=True)
    birth_date = models.DateField()
    death_date = models.DateField(blank=True, null=True)
    biography = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    photo = models.ImageField(blank=True, upload_to='author_photo/')

    def __str__(self):
        return self.second_name

    @property
    def full_name(self):
        return '%s %s %s' % (self.second_name,
                             self.first_name,
                             self.middle_name)

    def short_name(self):
        if self.pseudonym:
            return '{}'.format(self.pseudonym)
        elif self.middle_name:
            return '{} {}. {}.'.format(self.second_name,
                                       self.first_name[0].capitalize(),
                                       self.middle_name[0].capitalize())
        else:
            return '{} {}.'.format(self.second_name,
                                   self.first_name[0].capitalize())

    class Meta:
        ordering = ('second_name',)


class Book(Timestamp):
    title = models.CharField(unique=True, max_length=80)
    year = models.IntegerField()
    number_page = models.IntegerField()
    publishing = models.ForeignKey(PublishingHouse, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, through='BookAuthor')
    genre = models.ManyToManyField(Genre)
    description = models.TextField()
    cover = models.ImageField(blank=True, upload_to='book_cover/')
    ratings = GenericRelation(Rating, related_query_name='books')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_info', kwargs={'pk': self.pk})


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        auto_created = True


class User(AbstractUser):
    is_reader = models.BooleanField(default=True)
    is_publisher = models.BooleanField(default=False)
    is_subscription = models.BooleanField(verbose_name='send email', default=False)
    middle_name = models.CharField(max_length=25, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(verbose_name='email address', unique=True, error_messages={
                              'unique': "A user with that email already exists.",
                              })


class Publisher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,
                                related_name='publisher_profile')
    publishing_house = models.ForeignKey(PublishingHouse, on_delete=models.CASCADE, blank=True)


class Invitation(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_token = models.UUIDField(max_length=36, default=uuid.uuid4, editable=False, unique=True)

    def send(self):
        subject = 'You have been invited to signup to Library'
        context = dict(url=''.join([get_current_site(None).domain, self.get_absolute_url()]))
        message = render_to_string('registration/invitation_email.html', context)
        mail_from = settings.EMAIL_FROM
        mail_to = self.user.email
        send_mail(subject, message, mail_from, [mail_to])

    def get_absolute_url(self):
        return reverse('invitation', kwargs={'token': self.auth_token})

    def is_valid(self):
        now = timezone.now()
        if (now-self.created_at).days >= settings.INVITATIONS_LIFETIME:
            return False
        return True


class Comment(Timestamp, MPTTModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')

