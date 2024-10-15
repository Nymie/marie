from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, EnfantForm
from .models import Enfant

# Vue pour l'inscription
def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscription réussie ! Vous pouvez vous connecter.')
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

# Vue pour la connexion
def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_type = getattr(user, 'user_type', None)
            # Redirige en fonction du type d'utilisateur
            if user_type == 'doctor':
                return redirect('doctor_dashboard')
            elif user_type == 'ong':
                return redirect('ong_dashboard')
            elif user_type == 'donateur':  # Corrigé de 'donor' à 'donateur'
                return redirect('donateur_dashboard')
            elif user_type == 'admin':
                return redirect('admin_dashboard')
            else:
                return render(request, 'erreur.html')  # Assurez-vous que ce template existe
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')

# Vue pour ajouter un enfant
@login_required
def ajouter_enfant(request):
    # Vérifie si l'utilisateur peut ajouter un enfant
    if request.user.user_type not in ['doctor', 'ong', ]:
        messages.error(request, 'Vous n\'avez pas la permission d\'ajouter un enfant.')
        return redirect('home')  # Redirige vers la page d'accueil ou une autre page

    if request.method == 'POST':
        form = EnfantForm(request.POST)
        if form.is_valid():
            enfant = form.save(commit=False)
            enfant.utilisateur = request.user  # Associe l'utilisateur connecté
            enfant.save()
            messages.success(request, 'Enfant ajouté avec succès !')
            return redirect('doctor_dashboard')  # Redirige vers le tableau de bord approprié
    else:
        form = EnfantForm()

    return render(request, 'ajouter-enfant.html', {'form': form})  # Rendu de la page avec le formulaire

# Vues pour les différents tableaux de bord
@login_required
def donateur_dashboard(request):
    # Les donateurs ne voient ni la liste ni le formulaire d'ajout d'enfant
    messages.info(request, 'Vous n\'avez pas la permission de voir ou d\'ajouter des enfants.')
    return render(request, 'donateur/donateur_dashboard.html')

@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')


def widgets(request):
    return render(request, 'widgets.html')  # Assurez-vous que le chemin vers le template est correct


@login_required
def ong_dashboard(request):
    return render(request,)

@login_required
def admin_dashboard(request ):
    return render(request, 'admin_dashboard.html')
  








# Vue pour la déconnexion
def deconnexion(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté avec succès.')
    return redirect('connexion')


