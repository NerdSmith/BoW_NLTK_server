import base64
import json
import pickle

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from business.BoW import collect_dataset, word_to_count, get_most_frequently, get_sentence_vectors
from pages.forms import BoWForm
from pages.models import Post, to_table


class OwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user and not self.request.user.is_superuser:
            return HttpResponseForbidden()
        return super(OwnerMixin, self).dispatch(request, *args, **kwargs)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_list.html'


    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class HomePageView(TemplateView):
    template_name = 'home.html'


class PostDetailView(OwnerMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreateView(View):
    form_class = BoWForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        return render(request, "post_new.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            pass

            if request.user.is_authenticated:
                p = Post.objects.create(title=form.cleaned_data['title'], author=request.user, body=form.cleaned_data['body'])
                p.save()

                return redirect(reverse('post_detail', args=(p.id,)))

            else:
                title = form.cleaned_data['title']
                body = form.cleaned_data['body']

                dataset = collect_dataset(body)
                w2c = word_to_count(dataset)
                freq_words = get_most_frequently(w2c, 20)
                s_vectors = get_sentence_vectors(dataset, freq_words)

                freq_words_json = json.dumps(freq_words)
                np_bytes = pickle.dumps(s_vectors)

                np_base64 = base64.b64encode(np_bytes)

                table = to_table(freq_words_json, np_base64)

                return render(request, 'post_detail_guest.html', {'title': title, 'body': body, 'table': table})

        return render(request, 'post_new.html', {'form': form})



    # model = Post
    # template_name = 'post_new.html'
    # fields = ('title', 'body')
    #
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)