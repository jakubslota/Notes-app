from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
from django.db.models import Q
from django.utils.dateparse import parse_date
# Create your views here.

@login_required
def notes_list(request):

    qs = Note.objects.filter(owner=request.user)

    q = request.GET.get('q', '').strip()
    date_from = request.GET.get('from', '').strip()
    date_to = request.GET.get('to', '').strip()
    sort = request.GET.get('sort', 'new').strip()

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
    
    d_from = parse_date(date_from) if date_from else None
    d_to = parse_date(date_to) if date_to else None

    if d_from:
        qs = qs.filter(created_at__date__gte=d_from)

    if d_to:
        qs = qs.filter(created_at__date__lte=d_to)

    if sort == 'old':
        qs = qs.order_by('created_at')
    else:
        qs = qs.order_by('-created_at')
    
    context = {
        'notes': qs,
        'filters': {
            'q': q,
            'from': date_from,
            'to': date_to,
            'sort': sort,
        },
    }


    return render(request, "notes/notes_list.html",context)

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

    return render(request, template_name, {'form': form, 'mode':'create'})

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

    return render(request, template_name, {'form': form, 'mode':'edit'})

@login_required
def note_delete(request, pk, template_name='notes/note_confirm_delete.html'):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes:notes_list')
    return render(request, template_name, {'note': note})