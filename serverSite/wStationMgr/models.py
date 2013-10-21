from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey, _get_base_polymorphic_model
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.http import  HttpResponse
from django.utils.safestring import mark_safe
from django.utils import simplejson
import mptt, json

# Create your models here.
# A base model for the tree:


class PolymorphicTreeForeignKeyCustom(PolymorphicTreeForeignKey):

     default_error_messages = {
        'no_children_allowed': _("The selected node cannot have child nodes."),
	'no_parent_allowed': _("The Node %s cannot have %s as parent. Allowed parents : %s."),
     }

     def _validate_parent(self, parent, model_instance):
        if not parent:
            return
        elif isinstance(parent, (int, long)):
            # TODO: Improve this code, it's a bit of a hack now because the base model is not known in the NodeTypePool.
            base_model = _get_base_polymorphic_model(model_instance.__class__)

            # Get parent, TODO: needs to downcast here to read can_have_children.
            parent = base_model.objects.get(pk=parent)
        elif not isinstance(parent, PolymorphicMPTTModel):
            raise ValueError("Unknown parent value")
        
        if not model_instance.node_type:
		model_instance.node_type = NodeType.objects.get( name = model_instance.__class__.__name__ )

	allowed_parents = model_instance.node_type.allowed_parents.all().values_list("name", flat=True)
        if parent.can_have_children:
		if not allowed_parents or parent.__class__.__name__ in allowed_parents:
			return
		else:
			raise ValidationError( self.error_messages['no_parent_allowed'] % ( model_instance.__class__.__name__, parent.__class__.__name__, ' , '.join(allowed_parents)) )	

        raise ValidationError(self.error_messages['no_children_allowed']) 	


class NodeType(models.Model):
    name = models.CharField( max_length=50, unique=True )
    allowed_parents = models.ManyToManyField( 'NodeType', null=True, blank=True )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name 


class BaseTreeNode(PolymorphicMPTTModel):
    parent = PolymorphicTreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name=_('parent'))
    node_type = models.ForeignKey( NodeType )
    title = models.CharField(_("Title"), max_length=200)
    name = models.CharField( max_length=25, unique=True )
    description = models.CharField( max_length=100, null=True, blank=True )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)	
    active = models.BooleanField(default=True)

    
    def save(self, *args, **kwargs):
        self.node_type = NodeType.objects.get( name = self.__class__.__name__ )
	super(BaseTreeNode, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.title

    def get_show_data(self):
	    return mark_safe( json.dumps( self.get_data() ).replace("\"", "'") )

    def get_data(self):
 	    data = { 'title' : self.title, 'description' : self.description }	
	    return data	
	
    def get_immediate_nodes(self):
       	    return BaseTreeNode.objects.filter( parent = self.id, active = True )

    def get_verbose_name(self):
    	    return self._meta.verbose_name

    def get_allowed_parents(self):
    	    return []

    nodes_list = property( get_immediate_nodes );

    class Meta:
        verbose_name = _("Tree node")
        verbose_name_plural = _("Tree nodes")


# Server entity
class Network(BaseTreeNode):
    security_protocol = models.CharField( max_length=50 )
   
    def __unicode__(self):
        return self.name

    def get_data(self):
	    data = { 'type' :  Network._meta.verbose_name.title() , 'title' : self.title, 'description' : self.description, 'security_protocol' : self.security_protocol }	
	    return data	
	
    def get_allowed_parents(self):
    	    return ['Network']

    class Meta:
        verbose_name = _("Network")
        verbose_name_plural = _("Network nodes")
	

# Server entity
class Server(BaseTreeNode):
    
    OS_CHOICES = (
        ('Unix', 'Sistema operativo Unix '),
        ('Windows', 'Windows 2000|7|8'),
	('Solaris', 'Solaris'),
	('Max', 'Mac OS X'),
    )

    ip_address = models.CharField( max_length=20 )
    os = models.CharField( max_length=30, choices=OS_CHOICES ) 

    def __unicode__(self):
        return self.name


    def get_data(self):
	    data = { 'os' : self.os, 'type' : Server._meta.verbose_name.title(), 'title' : self.title, 'ip' : self.ip_address, 'description' : self.description }	
	    return data	

    def get_allowed_parents(self):
    	    return ['Network', 'Server']

    class Meta:
        verbose_name = _("Server")
        verbose_name_plural = _("Server nodes")
    

# Logical Device
class LogicalDevice(BaseTreeNode):
    ref = models.CharField( max_length=20 )

    def __unicode__(self):
        return self.name


    def get_data(self):
	    data = { 'type' : LogicalDevice._meta.verbose_name.title(), 'title' : self.title, 'ref' : self.ref, 'description' : self.description }	
	    return data	

    def get_allowed_parents(self):
    	    return ['Server']

    class Meta:
        verbose_name = _("Logical Device")
        verbose_name_plural = _("Locial Devices nodes")
    
    
# Logical Node
class LogicalNode(BaseTreeNode):
    ref = models.CharField( max_length=20 )

    def __unicode__(self):
        return self.name


    def get_data(self):
	    data = { 'type' : LogicalNode._meta.verbose_name.title(), 'title' : self.title, 'ref' : self.ref, 'description' : self.description }	
	    return data	

    def get_allowed_parents(self):
    	    return ['LogicalDevice']

    class Meta:
        verbose_name = _("Logical Node")
        verbose_name_plural = _("Logical Node nodes")
    

# Data
class Data(BaseTreeNode):
    ref = models.CharField( max_length=20 )
    presence = models.CharField( max_length=20 )
    
    can_have_children = False

    def __unicode__(self):
        return self.name
    

    def get_data(self):
	return { 'type' : Data._meta.verbose_name.title(), 
	 	     'title' : self.title, 
		     'ref' : self.ref, 
		     'presence' : self.presence,
		     'attribute datas' : self.get_attribute_data_set(),
		     'composite datas' : self.get_composite_data_set()
		   }	

    def get_composite_data_set(self):
	comp_map = list()
	for composite_data in self.composite_datas.all():
	        current = {}
		current['name'] = composite_data.name 
		current['ref'] = composite_data.ref
		current['presence'] = composite_data.presence
		current['id'] = composite_data.id
		comp_map.append( current )
	
	return comp_map

	
    def get_attribute_data_set(self):
	attr_map = list()
	for attr_data in self.attr_datas.all():
	        current = {}
		current['id'] = attr_data.id
		current['functional constraint'] = {}
		current['functional constraint']['name'] = attr_data.functional_constraint.name 
		current['functional constraint']['semantic'] = attr_data.functional_constraint.semantic 
		current['attribute type data'] = {}
		current['attribute type data']['name'] = attr_data.attribute_type_data.name
		current['attribute type data']['ref'] = attr_data.attribute_type_data.ref
		current['attribute type data']['presence'] = attr_data.attribute_type_data.presence
		current['attribute type data']['basic type'] = {}
		current['attribute type data']['basic type']['name'] = attr_data.attribute_type_data.basic_type.name
		current['attribute type data']['basic type']['length'] = attr_data.attribute_type_data.basic_type.length
		attr_map.append( current )
	
	return attr_map

    class Meta:
        verbose_name = _("Data")
        verbose_name_plural = _("Data nodes")

# Composite Data
class CompositeData(models.Model):
    name = models.CharField( max_length=50 )
    ref = models.CharField( max_length=20 )
    presence = models.CharField( max_length=20 )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    data = models.ForeignKey( Data, related_name = 'composite_datas' )

    def __unicode__(self):
        return self.name
    


# Basic Type
class BasicType(models.Model):
    name = models.CharField( max_length=15 )
    length = models.IntegerField( max_length=10, null=True, blank=True, default=5 )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
    


# Functional Constraint
class FunctionalConstraint(models.Model):
    name = models.CharField( max_length=50 )
    semantic = models.CharField( max_length=50 )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
	    return  self.name


# AttributeTypeData
class AttributeTypeData(models.Model):
    name = models.CharField( max_length=50 )
    ref = models.CharField( max_length=20 )
    presence = models.CharField( max_length=20 )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    basic_type = models.OneToOneField( BasicType )

    def __unicode__(self):
	    return self.name


# Attribute
class AttributeData(models.Model):
    data = models.ForeignKey( Data,  related_name='attr_datas' )   
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    attribute_type_data = models.ForeignKey( AttributeTypeData, related_name='attr_datas' )
    functional_constraint = models.ForeignKey( FunctionalConstraint, related_name='attr_datas' )

    def __unicode__(self):
	    return str(self.id)
    
# Composite Component
class CompositeComponent(models.Model):
    name = models.CharField( max_length=50 )
    ref = models.CharField( max_length=20 )
    presence = models.CharField( max_length=50 )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    attribute_type_data = models.ForeignKey( AttributeTypeData, related_name = 'composite_components' )	


    def __unicode__(self):
        return self.name   


    
