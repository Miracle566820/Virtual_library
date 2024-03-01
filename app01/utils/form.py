from app01 import models
from django import forms
from app01.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):

    class Meta:
        model = models.Book
        fields = "__all__"

