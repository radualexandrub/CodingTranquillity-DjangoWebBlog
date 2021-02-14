from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(
				request, "Your account was created! Welcome aboard, {}!".format(username))
			return redirect('login')
	else:
		form = UserRegisterForm()

	return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
	# Update User Info (in Profile)
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		if u_form.is_valid():
			u_form.save()
			messages.success(
				request, "Your profile has been updated!")
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)

	context = {
		'u_form': u_form
	}
	return render(request, 'users/profile.html', context)

# messages.debug()
# messages.info()
# messages.warning()
# messages.error()

# from django.contrib.auth.decorators import login_required, permission_required
# @permission_required('MainApp.add_blogpost', login_url="index")
