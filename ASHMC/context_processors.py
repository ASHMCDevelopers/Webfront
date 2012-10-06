from ASHMC.main.forms import LandingLoginForm


def add_login_form(request):
    if request.user.is_authenticated():
        return {}

    #print "Adding login form."

    return {'login_form': LandingLoginForm()}
