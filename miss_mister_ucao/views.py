from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Miss, Vote

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Prend la première IP derrière un proxy
    else:
        ip = request.META.get('REMOTE_ADDR')  # Adresse IP directe
    return ip


def miss_list(request):
    # Récupérer toutes les candidates avec le nombre de votes
    misses = Miss.objects.annotate(vote_count=Count('votes'))
    total_votes = sum(miss.vote_count for miss in misses)  # Total des votes

    # Gestion de la recherche
    search_query = request.GET.get('search', '')
    if search_query:
        misses = misses.filter(name__icontains=search_query)

    # Tri des candidates
    sort_by = request.GET.get('sort', 'none')  # Par défaut, pas de tri
    if sort_by == 'name_asc':
        misses = misses.order_by('name')
    elif sort_by == 'name_desc':
        misses = misses.order_by('-name')
    elif sort_by == 'votes_asc':
        misses = misses.order_by('vote_count')
    elif sort_by == 'votes_desc':
        misses = misses.order_by('-vote_count')

    # Calculer le pourcentage de votes pour chaque candidate
    for miss in misses:
        miss.vote_percentage = round((miss.vote_count / total_votes) * 100, 2) if total_votes > 0 else 0

    # Pagination
    paginator = Paginator(misses, 5)  # 5 candidates par page
    page_number = request.GET.get('page')
    misses = paginator.get_page(page_number)

    return render(request, "miss_list.html", {"misses": misses, "sort_by": sort_by, "search_query": search_query, "total_votes": total_votes})

def vote(request, miss_id):
    if request.method == "POST":
        ip = get_client_ip(request)

        # Vérifie si l'utilisateur a déjà voté
        if Vote.objects.filter(ip_address=ip).exists():
            return JsonResponse({"success": False, "message": "Vous avez déjà voté !"}, status=400)

        miss = get_object_or_404(Miss, id=miss_id)
        Vote.objects.create(ip_address=ip, miss=miss)

        # Compter le nombre de votes mis à jour
        vote_count = miss.votes.count()

        # Calculer le pourcentage de votes mis à jour
        total_votes = Vote.objects.count()
        vote_percentage = round((vote_count / total_votes) * 100, 2) if total_votes > 0 else 0

        return JsonResponse({
            "success": True,
            "message": f"Vote enregistré pour {miss.name} !",
            "vote_percentage": vote_percentage,
            "miss_id": miss_id
        })

    return JsonResponse({"success": False, "message": "Méthode non autorisée"}, status=405)

def get_results(request):
    # Récupérer les données pour le graphique
    misses = Miss.objects.annotate(vote_count=Count('votes'))
    total_votes = sum(miss.vote_count for miss in misses)  # Total des votes

    # Calculer le pourcentage de votes pour chaque candidate
    labels = [miss.name for miss in misses]
    votes = [round((miss.vote_count / total_votes) * 100, 2) if total_votes > 0 else 0 for miss in misses]

    return JsonResponse({"labels": labels, "votes": votes})