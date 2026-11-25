from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Azienda, Profilo, Dipendente, RichiestaFerie

@login_required
def dashboard(request):
    # ... (il codice che già hai per la dashboard) ...
    # (Non toccare questa parte, lasciala com'è)
    profilo = Profilo.objects.get(user=request.user)
    azienda = profilo.azienda
    dipendenti = Dipendente.objects.filter(azienda=azienda)
    
    if request.method == 'POST':
        dipendente_id = request.POST.get('dipendente_id')
        data_inizio = request.POST.get('data_inizio')
        data_fine = request.POST.get('data_fine')
        note = request.POST.get('note')
        
        dipendente = Dipendente.objects.get(id=dipendente_id)
        RichiestaFerie.objects.create(
            dipendente=dipendente,
            data_inizio=data_inizio,
            data_fine=data_fine,
            note=note
        )
        return redirect('dashboard')
    
    richieste = RichiestaFerie.objects.filter(dipendente__azienda=azienda).order_by('-id')
    
    context = {
        'azienda': azienda,
        'dipendenti': dipendenti,
        'richieste': richieste,
    }
    return render(request, 'personale/dashboard.html', context)

@login_required
def gestione_ferie(request):
    # ... (il codice che già hai per la gestione ferie) ...
    # (Non toccare questa parte, lasciala com'è)
    profilo = Profilo.objects.get(user=request.user)
    azienda = profilo.azienda
    
    richieste_in_attesa = RichiestaFerie.objects.filter(
        dipendente__azienda=azienda, 
        stato='In attesa'
    ).order_by('data_inizio')
    
    if request.method == 'POST':
        richiesta_id = request.POST.get('richiesta_id')
        azione = request.POST.get('azione')
        richiesta = RichiestaFerie.objects.get(id=richiesta_id)
        
        if azione == 'approva':
            richiesta.stato = 'Approvata'
            giorni = (richiesta.data_fine - richiesta.data_inizio).days + 1
            dipendente = richiesta.dipendente
            dipendente.ferie_residue -= giorni
            dipendente.save()
            richiesta.save()
        elif azione == 'rifiuta':
            richiesta.stato = 'Rifiutata'
            richiesta.save()
        return redirect('gestione_ferie')
        
    context = {
        'azienda': azienda,
        'richieste': richieste_in_attesa
    }
    return render(request, 'personale/gestione_ferie.html', context)

# NUOVA FUNZIONE PER LA REGISTRAZIONE
def registrazione(request):
    if request.method == 'POST':
        nome_azienda = request.POST.get('nome_azienda')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Creiamo l'azienda
        azienda = Azienda.objects.create(nome=nome_azienda)
        
        # Creiamo l'utente
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Il segnale post_save crea automaticamente il Profilo con un'azienda di default
        # Dobbiamo aggiornare il profilo con l'azienda appena creata
        profilo = Profilo.objects.get(user=user)
        profilo.azienda = azienda
        profilo.save()
        
        # Facciamo il login automatico dopo la registrazione
        login(request, user)
        return redirect('dashboard')
        
    return render(request, 'personale/registrazione.html')

@login_required
def aggiungi_dipendente(request):
    profilo = Profilo.objects.get(user=request.user)
    azienda = profilo.azienda
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        email = request.POST.get('email')
        data_assunzione = request.POST.get('data_assunzione')
        ruolo = request.POST.get('ruolo')
        ferie_residue = request.POST.get('ferie_residue')
        
        Dipendente.objects.create(
            azienda=azienda,
            nome=nome,
            cognome=cognome,
            email=email,
            data_assunzione=data_assunzione,
            ruolo=ruolo,
            ferie_residue=ferie_residue
        )
        return redirect('dashboard')
        
    return render(request, 'personale/aggiungi_dipendente.html')

@login_required
def elimina_dipendente(request, dipendente_id):
    profilo = Profilo.objects.get(user=request.user)
    azienda = profilo.azienda
    
    try:
        dipendente = Dipendente.objects.get(id=dipendente_id, azienda=azienda)
        dipendente.delete()
    except Dipendente.DoesNotExist:
        pass
        
    return redirect('dashboard')