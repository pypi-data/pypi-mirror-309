from datetime import datetime
from typing import Set
from oslc4py_client.Link import Link
from oslc4py_client.OSLCResource import OSLCResource
from oslc4py_domains_auto.ParameterInstance import ParameterInstance
from oslc4py_client.annotation_types.Occurs import Occurs
from oslc4py_client.annotation_types.ValueType import ValueType
from oslc4py_client.annotation_types.Representation import Representation
from oslc4py_client.decorators import oslc_name, oslc_namespace, oslc_property_definition, oslc_description, oslc_occurs, oslc_resource_shape, oslc_value_type, oslc_range, oslc_read_only, oslc_representation
from oslc4py_domains_auto.oslc_constants import NS_DCTERMS, NS_FOAF, NS_OSLC, NS_OSLC_AUTO, NS_RDF

@oslc_namespace(NS_OSLC_AUTO)
@oslc_name("AutomationRequest")
@oslc_resource_shape(describes=NS_OSLC_AUTO["AutomationRequest"], title="AutomationRequest Resource Shape")
class AutomationRequest(OSLCResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._contributor = set()
        self._created = None
        self._creator = set()
        self._description = None
        self._identifier = None
        self._modified = None
        self._type = set()
        self._title = None
        self._instance_shape = set()
        self._service_provider = set()
        self._state = set()
        self._desired_state = None
        self._input_parameter = set()
        self._executes_automation_plan = None
        self._produced_automation_result = None

    @property
    @oslc_name("contributor")
    @oslc_property_definition(NS_DCTERMS["contributor"])
    @oslc_description("Contributor or contributors to the resource.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_range(NS_FOAF["Person"])
    @oslc_read_only(False)
    def contributor(self):
        return self._contributor

    @contributor.setter
    def contributor(self, value: Set[Link]):
        self._contributor = value

    def add_contributor(self, value: Link):
        self._contributor.add(value)
    
    @property
    @oslc_name("created")
    @oslc_property_definition(NS_DCTERMS["created"])
    @oslc_description("Timestamp of resource creation")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.DATETIME)
    @oslc_read_only(False)
    def created(self):
        return self._created

    @created.setter
    def created(self, value: datetime):
        self._created = value

    @property
    @oslc_name("creator")
    @oslc_property_definition(NS_DCTERMS["creator"])
    @oslc_description("Creator or creators of the resource.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_range(NS_FOAF["Person"])
    @oslc_read_only(False)
    def creator(self):
        return self._creator

    @creator.setter
    def creator(self, value: Set[Link]):
        self._creator = value

    def add_creator(self, value: Link):
        self._creator.add(value)
    @property
    @oslc_name("description")
    @oslc_property_definition(NS_DCTERMS["description"])
    @oslc_description("Descriptive text about resource represented as rich text.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.XMLLITERAL)
    @oslc_read_only(False)
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    @oslc_name("identifier")
    @oslc_property_definition(NS_DCTERMS["identifier"])
    @oslc_description("A unique identifier for a resource.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.STRING)
    @oslc_read_only(False)
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value: str):
        self._identifier = value

    @property
    @oslc_name("modified")
    @oslc_property_definition(NS_DCTERMS["modified"])
    @oslc_description("Timestamp of latest resource modification")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.DATETIME)
    @oslc_read_only(False)
    def modified(self):
        return self._modified

    @modified.setter
    def modified(self, value: datetime):
        self._modified = value

    @property
    @oslc_name("type")
    @oslc_property_definition(NS_RDF["type"])
    @oslc_description("The resource type URIs.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def type(self):
        return self._type

    @type.setter
    def type(self, value: Set[Link]):
        self._type = value

    def add_type(self, value:Link):
        self._type.add(value)
    
    @property
    @oslc_name("title")
    @oslc_property_definition(NS_DCTERMS["title"])
    @oslc_description("Title of the resource represented as rich text.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.XMLLITERAL)
    @oslc_read_only(False)
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    @property
    @oslc_name("instanceShape")
    @oslc_property_definition(NS_OSLC["instanceShape"])
    @oslc_description("The URI of a Resource Shape.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_representation(Representation.REFERENCE)
    @oslc_read_only(False)
    def instance_shape(self):
        return self._instance_shape

    @instance_shape.setter
    def instance_shape(self, value: Set[Link]):
        self._instance_shape = value

    def add_instance_shape(self, value:Link):
        self.instance_shape.add(value)
        
    @property
    @oslc_name("serviceProvider")
    @oslc_property_definition(NS_OSLC["serviceProvider"])
    @oslc_description("A link to the resource's OSLC Service Provider. There may be cases when the subject resource is available from a service provider that implements multiple domain specifications, which could result in multiple values for this property.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_representation(Representation.REFERENCE)
    @oslc_read_only(False)
    def service_provider(self):
        return self._service_provider

    @service_provider.setter
    def service_provider(self, value: Set[Link]):
        self._service_provider = value

    def add_service_provider(self, value:Link):
        self.service_provider.add(value)
    
    @property
    @oslc_name("state")
    @oslc_property_definition(NS_OSLC_AUTO["state"])
    @oslc_description("Used to indicate the state of the automation request.")
    @oslc_occurs(Occurs.ONE_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(True)
    def state(self):
        return self._state

    @state.setter
    def state(self, value: Set[Link]):
        self._state = value

    @property
    @oslc_name("desiredState")
    @oslc_property_definition(NS_OSLC_AUTO["desiredState"])
    @oslc_description("Used to indicate the desired state of the Automation Request.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def desired_state(self):
        return self._desired_state

    @desired_state.setter
    def desired_state(self, value: Link):
        self._desired_state = value

    @property
    @oslc_name("inputParameter")
    @oslc_property_definition(NS_OSLC_AUTO["inputParameter"])
    @oslc_description("Parameters provided when Automation Requests are created.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.LOCALRESOURCE)
    @oslc_range(NS_OSLC_AUTO["ParameterInstance"])
    @oslc_read_only(False)
    def input_parameter(self):
        return self._input_parameter

    @input_parameter.setter
    def input_parameter(self, value: Set[ParameterInstance]):
        self._input_parameter = value

    def add_input_parameter(self, value:ParameterInstance):
        self.input_parameter.add(value)
    
    @property
    @oslc_name("executesAutomationPlan")
    @oslc_property_definition(NS_OSLC_AUTO["executesAutomationPlan"])
    @oslc_description("Automation Plan run by the Automation Request.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_representation(Representation.REFERENCE)
    @oslc_range(NS_OSLC_AUTO["AutomationPlan"])
    @oslc_read_only(False)
    def executes_automation_plan(self):
        return self._executes_automation_plan

    @executes_automation_plan.setter
    def executes_automation_plan(self, value: Link):
        self._executes_automation_plan = value

    @property
    @oslc_name("producedAutomationResult")
    @oslc_property_definition(NS_OSLC_AUTO["producedAutomationResult"])
    @oslc_description("Automation Result produced by the Automation Request.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_range(NS_OSLC_AUTO["AutomationResult"])
    @oslc_read_only(False)
    def produced_automation_result(self):
        return self._produced_automation_result

    @produced_automation_result.setter
    def produced_automation_result(self, value: Link):
        self._produced_automation_result = value
