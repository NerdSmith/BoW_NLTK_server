import base64
import json
import pickle
import uuid

from django.db import models
from django.utils.safestring import mark_safe


class Post(models.Model):
     title = models.CharField(max_length=200)
     author = models.ForeignKey(
         'accounts.CustomUser',
         on_delete=models.CASCADE, blank=True, null=True)
     body = models.TextField()

     def __str__(self):
        return self.title


class BoW(models.Model):
    # slug = models.SlugField(unique=True, default=uuid.uuid1, primary_key=True)
    # slug = models.SlugField(unique=True, default=uuid.uuid1, primary_key=True)
    post = models.OneToOneField(
        Post,
        related_name="posts",
        on_delete=models.CASCADE,
        primary_key=True
    )
    words = models.TextField(null=True)
    np_field = models.BinaryField()


    def __str__(self):
        return self.post.title

    def table(self):
        return to_table(self.words, self.np_field)


def to_table(words, np_field):
    t = '<table class="table table-bordered">'

    t += '<tr>'
    t += '<th>Sentence №</th>'
    for word in json.loads(words):
        t += f'<th>{word}</th>'
    t += '</tr>'

    np_bytes = base64.b64decode(np_field)
    np_array = pickle.loads(np_bytes)

    for row_idx in range(len(np_array)):
        t += '<tr>'
        t += f'<th >{row_idx + 1}</th>'

        for i_idx in range(len(np_array[row_idx])):
            if np_array[row_idx][i_idx]:
                t += '<td id="busy"></td>'
            else:
                t += '<td id="free"></td>'

        t += '</tr>'

    t += '</table>'

    return mark_safe(t)
