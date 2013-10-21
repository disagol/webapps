from django.forms import widgets
from rest_framework import serializers, relations
from wStationMgr.models import Server,LogicalDevice,LogicalNode,Data,CompositeData,BasicType,FunctionalConstraint,AttributeTypeData,AttributeData,CompositeComponent, BaseTreeNode,Network


class BaseTreeNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseTreeNode
        fields = ('id', 'title', 'name', 'description', 'created_date', 'modified_date', 'active' )

    def to_native(self, obj):
    	ret = super(BaseTreeNodeSerializer, self).to_native ( obj )

	if isinstance( obj, Network ):
		ret['security_protocol'] = obj.security_protocol
	elif isinstance( obj, Server ):		
		ret['ip_address'] = obj.ip_address	
		ret['os'] = obj.os
	elif isinstance( obj, Data ):		
		ret['presence'] = obj.presence	
		ret['ref'] = obj.ref
	else:
		ret['ref'] = obj.ref

	return ret


class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = ('parent','title', 'name', 'description', 'security_protocol' )

class LogicalDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogicalDevice
        fields = ('parent','title', 'name', 'description', 'ref' )

class LogicalNodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogicalNode
        fields = ('parent','title', 'name', 'description', 'ref' )	


class ServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = ('parent','title', 'name', 'description', 'ip_address', 'os' )


class CompositeDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompositeData
        fields = ('id', 'name', 'ref','presence')


class CompositeComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompositeComponent
        fields = ('id', 'name', 'ref','presence')


class BasicTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasicType
        fields = ('id', 'name', 'length')

class FunctionalConstraintField(serializers.RelatedField):
    def to_native(self, value):       
	    return { "Name : %s, Semantic : %s" % (value.name, value.semantic) } 


class AttributeTypeDataField(serializers.RelatedField):
    def to_native(self, value):       
	    return { "Name : %s, Ref : %s, Presence : %s, basic_type : %s" % (value.name, value.ref, value.presence, value.basic_type) } 


class AttributeTypeDataSerializer(serializers.ModelSerializer):
     basic_type = BasicTypeSerializer(many=False)
     composite_components = CompositeComponentSerializer(many=True)

     class Meta:
        model = AttributeTypeData
        fields = ( 'id', 'name','presence','basic_type', 'composite_components')


class FunctionalConstraintSerializer(serializers.ModelSerializer):

    class Meta:
        model = FunctionalConstraint
        fields = ('id', 'name', 'semantic')	


class AttributeDataSerializer(serializers.ModelSerializer):
    functional_constraint = FunctionalConstraintSerializer(many=False)
    attribute_type_data = AttributeTypeDataSerializer(many=False)

    class Meta:
        model = AttributeData
        fields = ( 'id', 'functional_constraint','attribute_type_data')


class DataSerializer(serializers.ModelSerializer):
    attr_datas = AttributeDataSerializer(many=True)
    composite_datas = CompositeDataSerializer(many=True)

    class Meta:
        model = Data
        fields = ('id', 'title', 'name', 'description','attr_datas','composite_datas')





