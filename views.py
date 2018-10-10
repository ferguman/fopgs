from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass

pgqlv = PrivateGraphQLView.as_view(graphiql=True)
