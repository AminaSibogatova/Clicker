from django.contrib.auth import login, logout, authenticate
from .forms import UserForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Core, Boost
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import CoreSerializer, BoostSerializer


@login_required
def index(request):
    core = Core.objects.get(user=request.user)
    boosts = Boost.objects.filter(core=core)  # Достаем бусты пользователя из базы

    return render(request, 'index.html', {
        'core': core,
        'boosts': boosts,
    })


@api_view(['GET'])
@login_required
def call_click(request):
    core = Core.objects.get(user=request.user)
    is_levelup = core.click()
    if is_levelup:
        Boost.objects.create(core=core, price=core.level * 50, power=core.level * 20)
    core.save()

    return Response({
        'core': CoreSerializer(core).data,
        'is_levelup': is_levelup,
    })


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = self.queryset.filter(core=core)
        return boosts

    def partial_update(self, request, pk):
        boost = self.queryset.get(pk=pk)
        levelup = boost.levelup()
        if not levelup:
            return Response({'error': 'malo deneg'})
        old_boost_values, new_boost_values = levelup
        return Response({
            'old_boost_values': self.serializer_class(old_boost_values).data,
            'new_boost_values': self.serializer_class(new_boost_values).data,
        })




def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            core = Core(user=user)
            core.save()
            login(request, user)
            return redirect('index')

        return render(request, 'register.html', {'form': form})

    form = UserForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    form = UserForm()

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')

        return render(request, 'login.html', {'form': form, 'invalid': True})

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


