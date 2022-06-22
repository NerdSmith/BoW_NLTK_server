import base64
import json
import pickle

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, BoW
from business.BoW import collect_dataset, word_to_count, get_most_frequently, get_sentence_vectors


@receiver(post_save, sender=Post)
def make_BoW(sender, instance, created, **kwargs):
    if created:
        body = instance.body

        dataset = collect_dataset(body)
        w2c = word_to_count(dataset)
        freq_words = get_most_frequently(w2c, 20)
        s_vectors = get_sentence_vectors(dataset, freq_words)

        freq_words_json = json.dumps(freq_words)
        np_bytes = pickle.dumps(s_vectors)

        np_base64 = base64.b64encode(np_bytes)

        BoW.objects.create(post=instance, words=freq_words_json, np_field=np_base64)

@receiver(post_save, sender=Post)
def save_BoW(sender, instance, **kwargs):
    instance.posts.save()
