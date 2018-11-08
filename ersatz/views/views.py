from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from ersatz.models import Product
from ersatz.views import toolbox
from ersatz.config import VIEWS_ERR, VIEWS_MSG_LOGIN


def search(request):
    context = toolbox.get_search_context(request)
    context.update({'form':'ersatz/searchform.html'})
    template = 'ersatz/no-result.html'

    # if status == True : there is some stuff to store in DB
    if context['status']:
        toolbox.update_db(context)
        template  = 'ersatz/result.html'

    return render(request, template, context)


def candidates(request, code):
    ersatz = toolbox.ErsatzProduct(code)
    context = ersatz.get_substitute_context()
    template = 'ersatz/no-candidates.html'

    if context['status']:
        template = 'ersatz/candidates.html'

    return render(request, template, context)


def favorite(request, e_code, p_code):
    """ Save to favorite if user is authenticated """

    context = {
        'status': False,
        'error': VIEWS_MSG_LOGIN,
        'form': 'account/anonymous.html',
    }
    template = 'ersatz/no-result.html'

    if request.user.is_authenticated:
        context = toolbox.save_favorite(request.user.id, e_code, p_code)
        template = 'ersatz/favorite.html'

    return render(request, template, context)


def favorite_list(request):
    """ List user's favorite """

    context = {
        'status': False,
        'message': VIEWS_MSG_LOGIN,
    }

    if request.user.is_authenticated:
        context = toolbox.list_favorite(request.user.id)

    return render(request, 'ersatz/list.html', context)


def product(request, code):
    """ Shows product details """

    context = {
        'status': False,
    }

    try:
        context['product'] = Product.objects.values().get(code=code)
    except (
            SyntaxError,
            NameError,
            ObjectDoesNotExist
    ) as except_detail:
        context['error'] = VIEWS_ERR.format(except_detail)
    else:
        context['status'] = True

    return render(request, 'ersatz/product.html', context)
