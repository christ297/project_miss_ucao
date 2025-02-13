from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Miss, Vote



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Prend la première IP derrière un proxy
    else:
        ip = request.META.get('REMOTE_ADDR')  # Adresse IP directe
    return ip





def miss_list(request):
    misses = Miss.objects.all()
    return render(request, "miss_list.html", {"misses": misses})

def vote(request, miss_id):
    if request.method == "POST":
        ip = request.META.get("REMOTE_ADDR")

        # Vérifie si l'utilisateur a déjà voté
        if Vote.objects.filter(ip_address=ip).exists():
            return JsonResponse({"success": False, "message": "Vous avez déjà voté !"}, status=400)

        miss = get_object_or_404(Miss, id=miss_id)
        Vote.objects.create(ip_address=ip, miss=miss)

        # Compter le nombre de votes mis à jour
        vote_count = miss.votes.count()

        return JsonResponse({"success": True, "message": f"Vote enregistré pour {miss.name} !", "votes": vote_count})

    return JsonResponse({"success": False, "message": "Méthode non autorisée"}, status=405)
