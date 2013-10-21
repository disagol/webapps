# Create your views here.
from django.http import  Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from wStationMgr.models import Server, LogicalDevice, LogicalNode, BaseTreeNode, Network, Data,AttributeData,FunctionalConstraint
from wStationMgr.serializer import JSONSerializer
from wStationMgr.permissions import IsOwnerOrReadOnly

from django.core import serializers
from django.views import generic
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.renderers import JSONRenderer, XMLRenderer

from wStationMgr.serializers import BaseTreeNodeSerializer,DataSerializer,ServerSerializer,NetworkSerializer,LogicalDeviceSerializer,LogicalNodeSerializer
from django.contrib.auth import logout
from django.template import Context, Template
import json


class IndexView(generic.ListView):
    template_name = 'wStationMgr/index.html'
    context_object_name = 'root_list'
	
    def get_queryset(self):
        """Return the last five created servers."""
        return BaseTreeNode.objects.filter( 
		parent__isnull=True, active = True
	).order_by('-created_date')
		
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
	context['user'] = self.request.user
        return context

class DetailView(generic.DetailView):
    model = Server
    template_name = 'wStationMgr/tree.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        return context 
    

class ResultsView(generic.DetailView):
    model = Server
    template_name = 'wStationMgr/results.html'



def tree(request, node_id):
    response = {'view': 'my_view', 'response_code': 0}
    try:
        root = get_object_or_404(BaseTreeNode, pk=node_id, active=True) 
	root_childs = root.get_descendants().filter( active = True );
    except (KeyError, BaseTreeNode.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'wStationMgr/tree.html', {
            'error_message': "Node does not exist.",
        })
    else:
	return render(request, 'wStationMgr/tree.html', {
            'root': root,
            'root_childs': root_childs,
            'error_message': "",
        })   


def help(request):
    return render(request, 'wStationMgr/help.html', {} )


def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/wStationMgr')

	
def tree_json(request, node_id):	
    response = {'view': 'my_view', 'response_code': 0}
    
    try:
        root = get_object_or_404(BaseTreeNode, pk=node_id, active=True) 
	root_childs = root.get_descendants().filter( active = True );      	
    except (KeyError, BaseTreeNode.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'wStationMgr/tree.html', {
            'error_message': "Node does not exist.",
        })
    else:
	return render(request, 'wStationMgr/tree_json.html', {
	    'root': root,
            'root_childs': root_childs,
            'error_message': "You didn't select a choice.",
        })



## Api classes ##

class NodeList(APIView):
    """
    List all nodes, or create a new snippet.
    """
    def get_object(self, node_name):
        try:
            return BaseTreeNode.objects.get(name=node_name)
        except BaseTreeNode.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
	node_name = request.GET.get('name','')
	include_node = request.GET.get('includeNode','')

	if not node_name:
       		nodes = BaseTreeNode.objects.all()
	elif include_node:
		if  include_node=='true':
			nodes = self.get_object( node_name ).get_descendants( include_self = True ).filter( level__lte=1 )
		else:
			nodes = self.get_object( node_name ).get_descendants().filter( level__lte=1 )
	else:
		node = self.get_object( node_name )
		return Response ( BaseTreeNodeSerializer(node, many=False).data )

	serializer = BaseTreeNodeSerializer(nodes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BaseTreeNodeSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServerList(APIView):
   
    def post(self, request, format=None):
	print request.DATA    
        serializer = ServerSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NetworkList(APIView):
   
    def post(self, request, format=None):
	print request.DATA    
        serializer = NetworkSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogicalDeviceList(APIView):
   
    def post(self, request, format=None):
	print request.DATA    
        serializer = LogicalDeviceSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogicalNodeList(APIView):
   
    def post(self, request, format=None):
	print request.DATA    
        serializer = LogicalNodeSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class NodeDetail(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
	
    """
    Retrieve, update or delete a node instance.
    """
    def get_object(self, node_id):
        try:
            return BaseTreeNode.objects.get(pk=node_id)
        except BaseTreeNode.DoesNotExist:
            raise Http404

    def get(self, request, node_id, format=None):
        node = self.get_object(node_id)
        serializer = BaseTreeNodeSerializer(node)
        return Response( serializer.data )

    def put(self, request, node_id, format=None):
        node = self.get_object(node_id)
        serializer = BaseTreeNodeSerializer(node, data=request.DATA, partial=True )
	print node.name
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, node_id, format=None):
        node = self.get_object(node_id)
        node.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DataList(APIView):
    """
    List all data, or create a new snippet.
    """
    def get_object(self, data_name):
        try:
            return Data.objects.get( name=data_name )
        except Data.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
	data_name = request.GET.get('name','')
	data_constraint_filter = request.GET.get('fconstraint','')

	# filter data logic
	if data_name:
       		datas = self.get_object( data_name )
		serializer = DataSerializer(datas, many=False)		
	elif data_constraint_filter:
		f_constraint_obj = get_object_or_404( FunctionalConstraint, name = data_constraint_filter )
		attr_data_set = f_constraint_obj.attr_datas
		datas = Data.objects.filter( id__in = [ attr_data.data.id for attr_data in attr_data_set.all() ] )
		serializer = DataSerializer(datas, many=True)
	else:
		datas = Data.objects.all()
		serializer = DataSerializer(datas, many=True)
	
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DataSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DataDetail(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
        
    """
    Retrieve, update or delete a data instance.
    """
    def get_object(self, node_id):
        try:
            return Data.objects.get(pk=node_id)
        except Data.DoesNotExist:
            raise Http404

    def get(self, request, node_id, format=None):
        node = self.get_object(node_id)
        serializer = DataSerializer(node)
        return Response( serializer.data )

    def put(self, request, node_id, format=None):
        node = self.get_object(node_id)
        serializer = DataSerializer(node, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, node_id, format=None):
        node = self.get_object(node_id)
        node.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# get methods for accessing tree
