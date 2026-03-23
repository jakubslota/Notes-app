from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm

# Create your views here.

@login_required
def notes_list(request):

    notes = Note.objects.filter(owner=request.user).order_by("-created_at")

    return render(request, "notes/notes_list.html", {"notes": notes})

@login_required
def note_create(request, template_name='notes/note_form.html'):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            return redirect('notes:notes_list')
    else:
        form = NoteForm()

    return render(request, template_name, {'form': form})

@login_required
def note_edit(request, pk, template_name='notes/note_form.html'):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note.save()
            return redirect('notes:notes_list')
    else:
        form = NoteForm(instance=note)

    return render(request, template_name, {'form': form})

@login_required
def note_delete(request, pk, template_name='notes/note_confirm_delete.html'):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes:notes_list')
    return render(request, template_name, {'note': note})