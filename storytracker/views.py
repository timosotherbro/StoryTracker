from django.shortcuts import render, redirect, get_object_or_404
from .models import Story, Update
from django.http import HttpResponseNotAllowed

# HOME PAGE — list all stories
def story_list(request):
    stories = Story.objects.order_by('-updated_at')
    return render(request, 'storytracker/story_list.html', {'stories': stories})


# STORY DETAIL PAGE
def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    updates = story.updates.all()  # newest first (because of Meta ordering)
    return render(request, 'storytracker/story_detail.html',
                  {'story': story, 'updates': updates})


# ADD NEW STORY
def new_story(request):
    if request.method == 'POST':
        title = request.POST['title']
        genre = request.POST.get('genre', '')
        tags = request.POST.get('tags', '')
        summary = request.POST.get('summary', '')

        Story.objects.create(
            title=title,
            genre=genre,
            tags=tags,
            summary=summary,
        )
        return redirect('storytracker:story_list')

    return render(request, 'storytracker/new_story.html')


# EDIT STORY
def edit_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if request.method == 'POST':
        story.title = request.POST['title']
        story.genre = request.POST.get('genre', '')
        story.tags = request.POST.get('tags', '')
        story.summary = request.POST.get('summary', '')
        story.save()
        return redirect('storytracker:story_detail', story_id=story.id)

    return render(request, 'storytracker/edit_story.html', {'story': story})


# ADD NEW UPDATE
def new_update(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if request.method == 'POST':
        note = request.POST['note']
        words_added = request.POST.get('words_added', None)

        if words_added == '':
            words_added = None  # empty field should be stored as NULL

        Update.objects.create(
            story=story,
            note=note,
            words_added=words_added
        )
        return redirect('storytracker:story_detail', story_id=story.id)

    return render(request, 'storytracker/new_update.html', {'story': story})


# DELETE STORY (and all its updates via CASCADE)
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if request.method == 'POST':
        story.delete()
        return redirect('storytracker:story_list')

    # Only allow POST for safety
    return HttpResponseNotAllowed(['POST'])


# DELETE SINGLE UPDATE
def delete_update(request, update_id):
    update = get_object_or_404(Update, id=update_id)
    story_id = update.story.id  # remember where to go back

    if request.method == 'POST':
        update.delete()
        return redirect('storytracker:story_detail', story_id=story_id)

    # Only allow POST for safety
    return HttpResponseNotAllowed(['POST'])