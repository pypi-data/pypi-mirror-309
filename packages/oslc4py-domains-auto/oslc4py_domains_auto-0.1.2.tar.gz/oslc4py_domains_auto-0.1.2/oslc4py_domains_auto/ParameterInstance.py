from oslc4py_client.OSLCResource import OSLCResource
from oslc4py_client.annotation_types.Occurs import Occurs
from oslc4py_client.annotation_types.ValueType import ValueType
from oslc4py_client.decorators import oslc_name, oslc_namespace, oslc_occurs, oslc_property_definition, oslc_resource_shape, oslc_value_type
from oslc4py_domains_auto.oslc_constants import NS_DCTERMS, NS_OSLC, NS_OSLC_AUTO, NS_RDF

@oslc_namespace(NS_OSLC_AUTO)
@oslc_name("ParameterInstance")
@oslc_resource_shape(describes=NS_OSLC_AUTO["ParameterInstance"], title="ParameterInstance Resource Shape")
class ParameterInstance(OSLCResource):
    def __init__(self, about=None, **kwargs):
        super().__init__(**kwargs)
        self.value = None
        self.description = None
        self.type = set()
        self.instance_shape = set()
        self.service_provider = set()
        self.name = None

    def __str__(self, as_local_resource=False):
        if as_local_resource:
            return (f"{'--name=' + self.name + '<br>' if self.name else ''}"
                    f"{'--value=' + self.value + '<br>' if self.value else ''}"
                    f"{'--description=' + self.description + '<br>' if self.description else ''}"
                    f"{'--type=' + next(iter(self.type)).get_value() + '<br>' if self.type else ''}"
                    f"{'--instanceShape=' + next(iter(self.instance_shape)).get_value() + '<br>' if self.instance_shape else ''}"
                    f"{'--serviceProvider=' + next(iter(self.service_provider)).get_value() if self.service_provider else ''}")
        return str(self)

    def add_type(self, link):
        self.type.add(link)

    def add_instance_shape(self, link):
        self.instance_shape.add(link)

    def add_service_provider(self, link):
        self.service_provider.add(link)

    @property
    @oslc_name("value")
    @oslc_property_definition(NS_RDF["value"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.STRING)
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    @oslc_name("description")
    @oslc_property_definition(NS_DCTERMS["description"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.XMLLITERAL)
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    @oslc_name("type")
    @oslc_property_definition(NS_RDF["type"])
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    def type(self):
        return self._type

    @type.setter
    def type(self, type_set):
        self._type = type_set

    @property
    @oslc_name("instanceShape")
    @oslc_property_definition(NS_OSLC_AUTO["instanceShape"])
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    def instance_shape(self):
        return self._instance_shape

    @instance_shape.setter
    def instance_shape(self, instance_shape_set):
        self._instance_shape = instance_shape_set

    @property
    @oslc_name("serviceProvider")
    @oslc_property_definition(NS_OSLC_AUTO["serviceProvider"])
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    def service_provider(self):
        return self._service_provider

    @service_provider.setter
    def service_provider(self, service_provider_set):
        self._service_provider = service_provider_set

    @property
    @oslc_name("name")
    @oslc_property_definition(NS_OSLC["name"])
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.STRING)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
