from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, AvatarUpdateForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been succesfully created!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required # impide acceder a la view si no se está autenticado
def avatar(request):
    if request.method == 'POST':
        # las dos clases (u_form, a_form) recogerán la información de un sólo formulario
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AvatarUpdateForm(request.POST, request.FILES, instance=request.user.avatar)
        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()
            messages.success(request, f'Your account has been updated!') # mensaje flash a base.html
            return redirect('avatar')

    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AvatarUpdateForm(instance=request.user.avatar)

    context = { # los dos formularios se mostrarán como uno solo
        'u_form': u_form,
        'a_form': a_form
    }

    return render(request, 'users/avatar.html', context)
