from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from apprang.models import Category, Page
from apprang.forms import CategoryForm, PageForm


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
        category.url = category.name.replace(' ', '_')

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
    ##category_name = category_name_url.replace('_', ' ')
    ###SVM
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
