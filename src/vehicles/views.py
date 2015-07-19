from django.shortcuts import render, render_to_response, RequestContext
# import the custom context processor
from vehicles.context_processor import global_context_processor

from vehicles.models import Vehicle, Category


def home_page(request):
    return render_to_response("home_page.html", locals(),
        context_instance=RequestContext(request, processors=[global_context_processor]))


def category_page(request, slug):
    
    # check if make parameter is passed into the url
    vehicle_make = request.GET.get('make', None)
    # get category by slug
    category = Category.objects.get_category_by_slug(slug)
    # get all the vehicles by the category and make (if provided)
    vehicles_list = None
    if vehicle_make is not None:
        vehicles_list = Vehicle.objects.get_vehicles_by_category_and_make(
            category, vehicle_make)
    else:
        vehicles_list = Vehicle.objects.get_vehicles_by_category(category)
    
    return render_to_response("home_page.html", locals(),
        context_instance=RequestContext(request, processors=[global_context_processor]))


def get_makes_in_category(category):

    makes_in_category = []
    # get all the vehicle objects by category
    vehicles_in_category = Vehicle.objects.get_vehicles_by_category(category=category)
    for vehicle in vehicles_in_category:
        makes_in_category.append(vehicle.make)

    # remove duplicate makes from the list
    makes_in_category = list(set(makes_in_category))
    makes_in_category = sorted(makes_in_category, key=lambda x:x.v_make)

    return makes_in_category