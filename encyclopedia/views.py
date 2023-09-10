from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from . import util
import markdown2
import random as rand

class SearchFilter(forms.Form):
    q = forms.CharField(
        label='Search Encyclopedia',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'block h-full w-full border-transparent py-2 px-8 text-gray-900 placeholder-gray-500 focus:border-transparent focus:placeholder-gray-400 focus:outline-none focus:ring-0 sm:text-sm cursor-text', 'placeholder': 'Search...'
})
    )

class NewPost(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'block w-full border-0 py-2 px-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    content = forms.CharField(label="Content (Markdown)", widget=forms.Textarea(attrs={'class': 'block w-full border-0 py-2 px-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))

class EditPost(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'block w-full border-0 py-2 px-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    content = forms.CharField(label="Content (Markdown)", widget=forms.Textarea(attrs={'class': 'block w-full border-0 py-2 px-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))

# Homepage
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchFilter()
    })

# Search filter in the homepage
def search(request):
    if request.method == "GET": 
        form = SearchFilter(request.GET)
        if form.is_valid():
            query = form.cleaned_data['q'].lower()
            matching_entries = []
            for entry in util.list_entries():
                if query in entry.lower():
                    matching_entries.append(entry)

            if matching_entries:
                exact_match = None

                for entry in matching_entries:
                    if entry.lower() == query:
                        exact_match = entry
                        break
    
                if exact_match:
                    return HttpResponseRedirect(reverse("single-post", args=[exact_match]))

                return render(request, 'encyclopedia/search-results.html', {'query': query, 'entries': matching_entries})
                
    return HttpResponseRedirect(reverse("index"))

# Single post page
def single_post(request, title):
    get_page = util.get_entry(title)

    if get_page is None:
        return render(request, "encyclopedia/not-found.html", {'error_message': 'Page not found.'})
    
    markdown_content = markdown2.Markdown()
    get_page_html =  markdown_content.convert(get_page)
    return render(request, 'encyclopedia/single-post.html', {
        'title': title, 
        'content':  get_page_html, 
        'delete_url': reverse('delete-confirmation', args=[title])})

# Add new post
def post(request):
    if request.method == "POST":
        add_new_post = NewPost(request.POST)
        if add_new_post.is_valid():
            title = add_new_post.cleaned_data["title"]
            content = add_new_post.cleaned_data["content"]

            if util.get_entry(title) is not None:
                return render(request, 'encyclopedia/create-post.html', {
                    "new_post": add_new_post,
                    "error_message": "Post like this already exists.",
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("single-post", args=[title]))
    return render(request, 'encyclopedia/create-post.html', {
        "new_post": NewPost()
    })

# Edit post
def edit(request, title):
    existing_content = util.get_entry(title)
    if request.method == "POST":
        post = EditPost(request.POST)
        if post.is_valid():
            new_title = post.cleaned_data['title']
            new_post = post.cleaned_data['content']
            util.save_entry(new_title, new_post)
            return HttpResponseRedirect(reverse("single-post", args=[new_title]))
    else:
        post = EditPost(initial={'title':title, 'content': existing_content})
    return render(request, 'encyclopedia/edit-post.html', {
        'title': title,
        'post': post
    })

def random(request):
    entries = util.list_entries()
    if entries:
        random_title = rand.choice(entries)
        return HttpResponseRedirect(reverse("single-post", args=[random_title]))
    else:
        return HttpResponseRedirect(reverse("index"))

# Delete confirmation page
def delete_confirmation(request, title):
    return render(request, 'encyclopedia/delete-confirmation.html', {"title": title})

# Delete post
def delete_post(request, title):
    if request.method == "POST":
        util.delete_entry(title)
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("single-post", args=[title]))