import pdb

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

from apps.accounts.models import User
from apps.agents.forms import SingleAgentForm, AgencyForm
from apps.agents.models import Agent, Review
from apps.properties.models import Property, Comment
from propertyDealsIn9ja.utils import get_cities_only, get_states_only


class AgentListView(View):
    template_name = 'agents/list.html'

    def get(self, request, **kwargs):
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        states = get_states_only(file_path)
        agents = Agent.objects.all()
        featured_properties = Property.objects.filter(featured=True)

        context = {
            "agents": agents,
            "states": states,
            "featured_properties": featured_properties,
        }
        return render(request, self.template_name, context)


def filter_agents(request):
    agents = Agent.objects.all()
    file_path = "propertyDealsIn9ja/states-and-cities.json"
    states = get_states_only(file_path)
    agent_name_icontain_qs = request.GET.get("agent_name_icontain_qs")
    state_iexact_qs = request.GET.get("state_iexact_qs")
    city_iexact_qs = request.GET.get("city_iexact_qs")
    print(agent_name_icontain_qs, state_iexact_qs, city_iexact_qs)
    if agent_name_icontain_qs != '' and agent_name_icontain_qs is not None:
        agents = agents.filter(business_name__icontains=agent_name_icontain_qs)

    if state_iexact_qs != '' and state_iexact_qs is not None:
        agents = agents.filter(state__iexact=state_iexact_qs)

    if city_iexact_qs != '' and city_iexact_qs is not None:
        agents = agents.filter(city__iexact=city_iexact_qs)

    context = {
        "agents": agents,
        "states": states,
    }
    return render(request, 'agents/list.html', context)


class AgentDetailView(DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_object(self, **kwargs):
        return get_object_or_404(Agent, slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super(AgentDetailView, self).get_context_data()
        context['featured_properties'] = Property.objects.filter(featured=True)
        return context


class AgentReviewView(View):
    template_name = "agents/review_list.html"

    def post(self, request, slug):
        # agent_id = request.POST.get('agent_id')
        get_agent = get_object_or_404(Agent, slug=slug)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        obj, created = Review.objects.get_or_create(user=self.request.user)
        obj.user = request.user
        obj.agent = get_agent
        obj.rating = rating
        obj.comment = comment
        obj.save()
        get_agent.rating_aggregate = Review.objects.filter(agent=get_agent).aggregate(Avg('rating'))["rating__avg"]
        print(get_agent.rating_aggregate)
        get_agent.save(update_fields=['rating_aggregate'])
        return JsonResponse({'success': 'true', 'score': rating}, safe=False)


class AgentCreateView(LoginRequiredMixin, View):
    template_name = "agents/create.html"

    def get(self, request):
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        states = get_states_only(file_path)
        context = {
            "states": states,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Get form data from the request
        business_name = request.POST.get("business_name")
        business_email = request.POST.get("business_email")
        business_phone = request.POST.get("business_phone")
        business_logo = request.FILES.get("business_logo")  # Use FILES for file uploads
        state = request.POST.get("state")
        city = request.POST.get("city")
        street_address = request.POST.get("street_address")
        is_single_agent = request.POST.get("is_agentForm")

        print(f"""
            business_name: {business_name}
            business_email: {business_email}
            business_phone: {business_phone}
            business_logo: {business_logo}
            state: {state}
            city: {city}
            street_address: {street_address}
            is_single_agent: {is_single_agent} {type(is_single_agent)}
        """)
        # pdb.set_trace()
        agent = Agent.objects.create(
            business_user=request.user,
            business_name=business_name,
            business_email=business_email,
            business_phone=business_phone,
            business_logo=business_logo,  # Use FILES for file uploads
            state=state,
            city=city,
            street_address=street_address,
        )
        if is_single_agent != "True":
            agent.is_an_agency = True
            agent.save()
        agent.save()
        # Return a JSON response to the frontend
        return JsonResponse({
            "status": "success",
            "message": "Agent created successfully"
        })


class GetStateCities(View):
    templates = "agents/create.html"

    def post(self, request):
        state = request.POST['state']
        print(state)
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        cities = get_cities_only(file_path, state)
        data = {
            "cities": cities,
            "success": "request was successful cities populated..."
        }
        return JsonResponse(data=data, safe=False)


class GetMyReviews(View):
    templates = 'agents/user_review_list.html'

    def get(self, request):
        user = self.request.user
        agent = Agent.objects.get(business_user=user)
        agent_review_list = agent.agent_review.all()
        user_review_list = user.user_review.all()
        # get my properties..
        my_property_reviews = []
        my_uploaded_properties = user.agent.properties.all()
        print(my_uploaded_properties)
        for mp in my_uploaded_properties:
            # get comment for each property
            for c in Comment.objects.filter(property=mp):
                # append to my comment collection variable
                if c not in my_property_reviews:
                    print(c.by.username)
                    my_property_reviews.append(c)
                continue
        # pk_list = [obj.pk for obj in my_property_reviews]
        # my_property_reviews = Comment.objects.filter(pk__in=pk_list)
        print(my_property_reviews)
        context = {
            "agent_review_list": agent_review_list,
            "user_review_list": user_review_list,
            "my_property_reviews": my_property_reviews,
        }
        return render(request, self.templates, context)
#
# class GetMyReviews(View):
#     templates = 'agents/user_review_list.html'
#
#     def get(self, request):
#         user = self.request.user
#         agent = Agent.objects.get(business_user=user)
#         agent_review_list = agent.agent_review.all()
#         user_review_list = user.user_review.all()
#         my_property_reviews = agent.properties.comments.all()
#         context = {
#             "agent_review_list": agent_review_list,
#             "user_review_list": user_review_list,
#             "my_property_reviews": my_property_reviews,
#         }
#         return render(request, self.templates, context)
#
#
# class GetMyPropertReviews(View):
#     templates = 'agents/user_review_list.html'
#
#     def get(self, request):
#         user = self.request.user
#         agent = Agent.objects.get(business_user=user)
#         agent_review_list = agent.agent_review.all()
#         user_review_list = user.user_review.all()
#         my_property_reviews = agent.properties.comments.all()
#         context = {
#             "agent_review_list": agent_review_list,
#             "user_review_list": user_review_list,
#             "my_property_reviews": my_property_reviews,
#         }
#         return render(request, self.templates, context)

