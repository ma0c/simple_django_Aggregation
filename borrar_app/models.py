"""
This file contains the response for the question presented [here](https://gist.github.com/satya-waylit/180445cea4fbf5bca35150e3d1fc7529)

Attributes should be verbose, max_lenght in CharFields should be defined, required attributes should be marked as
null=False, as well the blanks for Text, define the `__str__` allows more readability. Foreign keys should have a
related name. All classes should be documented with DocStrings.

Solution to question 2 is in `UserProfile.get_all_profiles_with_job_ids` and assumes the usage of Postgres, however
it is possible to create an Aggregation function in case the engine doesn't support String aggregation

```
from django.db.models import Aggregate


class ArrayAgg(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)
```

Taked from [this Stack Overflow question](https://stackoverflow.com/questions/10340684/group-concat-equivalent-in-django/31337612#31337612)
and tested in SQLite
"""

from django.contrib.auth.models import User
from django.db.models import CharField
from django.db import models
from django.conf import settings


if "postgres" in settings.DATABASES['default']['ENGINE']:
    from django.contrib.postgres.aggregates import ArrayAgg
else:
    from django.db.models import Aggregate
    class ArrayAgg(Aggregate):
        function = 'GROUP_CONCAT'
        template = '%(function)s(%(distinct)s%(expressions)s)'

        def __init__(self, expression, distinct=False, **extra):
            super(ArrayAgg, self).__init__(
                expression,
                distinct='DISTINCT ' if distinct else '',
                output_field=CharField(),
                **extra)


class UserProfile(models.Model):
    """
    Extended information from `auth.User` model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(verbose_name="Date of Birth")

    @classmethod
    def get_all_profiles_with_job_ids(kls):
        """
        Single query that returns all UserProfile Objects annotated with the associated job_ids
        """
        return kls.objects.all().annotate(job_ids=ArrayAgg('user__jobs'))

    def __str__(self):
        return f"User Profile for: {self.user}"


class Job(models.Model):
    """
    Job representation for the application
    """
    title = models.CharField(verbose_name="Title", max_length=250, blank=False)
    description = models.TextField(verbose_name="Description", default="")
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")

    def __str__(self):
        return f"Job {self.title} for: {self.employee}"

