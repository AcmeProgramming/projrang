from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from apprang.models import Category, Page

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
    about_context_dict = {'boldmessage': "This is bold messaging information from about def"}

    """The template is in templates/apprang."""
    return render_to_response('apprang/about.html', about_context_dict, about_context)

def category(request, category_name_url):
    """The def category goes to category.html"""

    category_context = RequestContext(request)

    """The category_name holds category_name_url result after changing
        underscores to spaces.
        The category_name_url is a value passed from url."""
    category_name = category_name_url.replace('_', ' ')

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

        """Appending category to context_dict."""
        context_dict['category'] = category
    except Category.DoesNotExist:
        """If nothing in Category raise Category.DoesNotExist and pass."""
        pass

    """The template is in templates/apprang."""
    return render_to_response('apprang/category.html', context_dict, category_context)
