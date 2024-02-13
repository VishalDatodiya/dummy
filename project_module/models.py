from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField

from users.models import User


class AbstractTable(models.Model):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(AbstractTable):
    project_name = models.CharField(max_length=200)

    class Meta:
        db_table = "projects"

    def __str__(self):
        return str(self.project_name)


class Module(AbstractTable):
    user = models.ManyToManyField(User)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True,null=True)
    module_name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    body = RichTextField(default="")
   
    class Meta:
        db_table = "modules"

    def __str__(self):
        return str(self.module_name)
