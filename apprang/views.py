from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from apprang.models import Category, Page
from apprang.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


def decode_url(category_url_name):
    """Intention for def decode_url is to decode urls passed to it.
       Convert underscore to empty space, empty space to underscore."""
    if category_url_name.find("_") == -1:
        decoded_name = category_url_name.replace(' ', '_')
    else:
        """This is mainly how catalog_name_url in the other functions
           works now: replace('_', ' ')"""
        decoded_name = category_url_name.replace('_', ' ')
    return decoded_name



def index(request):
    """The def index goes to index.html."""

    context = RequestContext(request)

    """The category_list holds the query to Category table for a list
       of the top 5 items sorted by likes."""
    category_list = Category.objects.order_by('-likes')[:5]

    """The context_dict holds the category_list results in a hash.
       The template engine process hashs/dicts better."""
    context_dict = {'categories': category_list}

    """Working through category_list data to construct category.url
       for index template."""
    for category in category_list:
        ###category.url = category.name.replace(' ', '_')
        category.url = decode_url(category.name)

    """Adding Page objects to context_dict."""
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    """Creating sessions."""
    if request.session.get('last_visit'):
        """Session has value from last visit. """
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())

    else:
        """The get returns none and the sessions does not have a value."""
        request.session['last_vist'] = str(datetime.now())
        request.session['visits'] = 1

    """The template is in templates/apprang."""
    return render_to_response('apprang/index.html', context_dict, context)

def about(request):
    """The def about goes to about.html."""

    about_context = RequestContext(request)
    about_context_dict = {'boldmessage': "This is bold messaging information from def about"}

    """The template is in templates/apprang."""
    return render_to_response('apprang/about.html', about_context_dict, about_context)


def category(request, category_name_url):
    """The def category goes to category.html"""

    category_context = RequestContext(request)

    """The category_name holds category_name_url result after changing
        underscores to spaces.
        The category_name_url is a value passed from url."""
    category_name = decode_url(category_name_url)

    """The context_dict holds results from category_name"""
    context_dict = {'category_name': category_name}

    try:
        """The category holds the results returned by the query to
            Category."""
        category = Category.objects.get(name=category_name)

        """The pages holds the query from Page table."""
        pages = Page.objects.filter(category=category)

        """Appending pages to context_dict."""
        context_dict['pages'] = pages

        """Appending category_name_url to context_dict."""
        context_dict['category_name_url'] = category_name_url

        """Appending category to context_dict."""
        context_dict['category'] = category

    except Category.DoesNotExist:
        """If nothing in Category raise Category.DoesNotExist and pass."""
        pass

    """The template is in templates/apprang."""
    return render_to_response('apprang/category.html', context_dict, category_context)


###def add_category(request, category_name_url):
def add_category(request):
    """This def add_category allows categories to be added
       and goes to add_category.html""" 

    context = RequestContext(request)

    ###category_name = decode_url(category_name_url)
    """Checks if an HTTP POST"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        """Check of form is valid"""
        if form.is_valid():
            """Save data from form to database, in this case category."""
            form.save(commit=True)

            """Return user to index."""
            return index(request)

        else:
            """Print errors."""
            print form.errors
    else:
        """If request was not a POST, display the form."""
        form = CategoryForm()

    return render_to_response('apprang/add_category.html', {'form': form}, context)
    ##return render_to_response('apprang/add_category.html', 
            ##{'category_name_url': category_name_url,
             ##'category_name': category_name, 'form': form}, context)


def add_page(request, category_name_url):
    """This def add_page goes to add_page allowing page add."""
    context = RequestContext(request)

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)

            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response('apprang/add_category.html', {}, context)
                ##return render_to_response('apprang/add_category.html',
                        ##{'category_name_url': category_name_url, 'form': form}, context)

            page.views = 0
            page.save()
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response( 'apprang/add_page.html', 
            {'category_name_url': category_name_url,
             'category_name': category_name, 'form': form},
             context)

def register(request):
    """This def register handles registration"""
    context = RequestContext(request)

    """Boolean value for telling template whether the registration was
       successful.  Default is false.  Value changes to True when registration
       succeeds."""
    registered = False

    """If POST process data."""
    if request.method == 'POST':
        """Try to grab information from raw form.
           Making use of both UserForm and UserProfileForm."""
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        """If both forms are valid..."""
        if user_form.is_valid() and profile_form.is_valid():
            """Save user_form data to database."""
            user = user_form.save()

            """Hashing password with set_password method.
               Once hashed update user object."""
            user.set_password(user.password)
            user.save()

            """Sort out the UserProfile.
               Setting commit=False to delay saving model until we are
               ready to avoid integrity problems."""
            profile = profile_form.save(commit=False)
            profile.user = user

            """If profile picture was provided
               get it from input and put it in UserProfile model."""
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            """Now ready to save UserProfile model instance."""
            profile.save()

            """Update registered to tell template registration was successful."""
            registered = True

        else:
            """If form is invalid or any mistakes print errors."""
            most_errors = user_form.errors, profile_form.errors

    else:
        """If not an HTTP POST render form using two ModelForm instances."""
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('apprang/register.html', {'user_form': user_form,
                                                        'profile_form': profile_form,
                                                        'registered': registered}, context)


def user_login(request):
    """This def user_login handles user logging in after registration."""

    """This context holds the results from RequestContext of users request."""
    context = RequestContext(request)

    """If log in request is made, check if POST and collect username, password."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        """Check of password username combination is correct."""
        user = authenticate(username=username, password=password)

        """Mechanism to check if username, password combination is correct."""
        if user:
            """Check if account is active."""
            if user.is_active:
                """Process user request. Send to main page logged in."""
                login(request, user)
                return HttpResponseRedirect('/apprang/')
            else:
                """Notify that account is disabled."""
                return HttpResponse("Your account is disabled")
        else:
            """If invalid log in details inform.."""
            invalid_login_details = render_to_response('apprang/invalid.html', {}, context)
            return HttpResponse(invalid_login_details)

    else:
        """The request was not an HTTP POST so display login form."""
        return render_to_response('apprang/login.html', {}, context)


@login_required
def restricted(request):
    context = RequestContext(request)
    """This def restricted restricts sections to logged in users."""
    return render_to_response('apprang/restricted.html',{}, context)

@login_required
def user_logout(request):
    """Using django.contrib.auth.logout to log user out."""
    logout(request)
    """Redirect to home page."""
    return HttpResponseRedirect('/apprang/')
