from datetime import datetime
from typing import Set
from oslc4py_domains_auto.ParameterDefinition import ParameterDefinition
from oslc4py_client.annotation_types.Occurs import Occurs
from oslc4py_client.annotation_types.ValueType import ValueType
from oslc4py_client.OSLCResource import OSLCResource
from oslc4py_client.Link import Link
from oslc4py_client.decorators import oslc_description, oslc_name, oslc_namespace, oslc_occurs, oslc_property_definition, oslc_resource_shape, oslc_value_type, oslc_range, oslc_read_only
from oslc4py_domains_auto.oslc_constants import NS_DCTERMS, NS_FOAF, NS_OSLC, NS_OSLC_AUTO, NS_RDF

@oslc_namespace(NS_OSLC_AUTO)
@oslc_name("AutomationPlan")
@oslc_resource_shape(describes=NS_OSLC_AUTO["AutomationPlan"], title="AutomationPlan Resource Shape")
class AutomationPlan(OSLCResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._identifier = None
        self._title = None
        self._contributor = set()
        self._created = None
        self._creator = set()
        self._description = None
        self._modified = None
        self._type = set()
        self._subject = set()
        self._instance_shape = set()
        self._service_provider = set()
        self._parameter_definition = set()
        self._uses_execution_environment = set()
        self._future_action = set()

    @property
    @oslc_name("identifier")
    @oslc_property_definition(NS_DCTERMS["identifier"])
    @oslc_description("A unique identifier for the resource.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.STRING)
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = value

    @property
    @oslc_name("title")
    @oslc_property_definition(NS_DCTERMS["title"])
    @oslc_description("Title of the resource.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.STRING)
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    @oslc_name("contributor")
    @oslc_property_definition(NS_DCTERMS["contributor"])
    @oslc_description("Contributor or contributors to the resource. It is likely that the target resource will be a foaf:Person but that is not necessarily the case.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_range(NS_FOAF["Person"])
    @oslc_read_only(False)
    def contributor(self):
        return self._contributor

    @contributor.setter
    def contributor(self, value: Set[Link]):
        self._contributor = value

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
    @oslc_description("Creator or creators of the resource. It is likely that the target resource will be a foaf:Person but that is not necessarily the case.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_range(NS_FOAF["Person"])
    @oslc_read_only(False)
    def creator(self):
        return self._creator

    @creator.setter
    def creator(self, value: Set[Link]):
        self._creator = value

    @property
    @oslc_name("description")
    @oslc_property_definition(NS_DCTERMS["description"])
    @oslc_description("Descriptive text about resource represented as rich text in XHTML content. SHOULD include only content that is valid and suitable inside an XHTML <div> element.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type("XMLLiteral")
    @oslc_read_only(False)
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

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
    @oslc_description("The resource type URIs")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def type(self):
        return self._type

    @type.setter
    def type(self, value: Set[Link]):
        self._type = value

    @property
    @oslc_name("subject")
    @oslc_property_definition(NS_DCTERMS["subject"])
    @oslc_description("Tag or keyword for a resource. Each occurrence of a dcterms:subject property denotes an additional tag for the resource.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.STRING)
    @oslc_read_only(False)
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value: Set[str]):
        self._subject = value

    @property
    @oslc_name("instanceShape")
    @oslc_property_definition(NS_OSLC["instanceShape"])
    @oslc_description("The URI of a Resource Shape that describes the possible properties, occurrence, value types, allowed values and labels. This shape information is useful in displaying the subject resource as well as guiding clients in performing modifications.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def instance_shape(self):
        return self._instance_shape

    @instance_shape.setter
    def instance_shape(self, value: Set[Link]):
        self._instance_shape = value

    @property
    @oslc_name("serviceProvider")
    @oslc_property_definition(NS_OSLC["serviceProvider"])
    @oslc_description("A link to the resource's OSLC Service Provider.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def service_provider(self):
        return self._service_provider

    @service_provider.setter
    def service_provider(self, value: Set[Link]):
        self._service_provider = value

    @property
    @oslc_name("parameterDefinition")
    @oslc_property_definition(NS_OSLC_AUTO["parameterDefinition"])
    @oslc_description("The definition of a parameter for this Automation Plan.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.LOCALRESOURCE)
    @oslc_range(NS_OSLC_AUTO["ParameterDefinition"])
    @oslc_read_only(False)
    def parameter_definition(self):
        return self._parameter_definition

    @parameter_definition.setter
    def parameter_definition(self, value: Set[ParameterDefinition]):
        self._parameter_definition = value

    @property
    @oslc_name("usesExecutionEnvironment")
    @oslc_property_definition(NS_OSLC_AUTO["usesExecutionEnvironment"])
    @oslc_description("A resource representing the environment(s) which this Automation Plan can be executed in.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def uses_execution_environment(self):
        return self._uses_execution_environment

    @uses_execution_environment.setter
    def uses_execution_environment(self, value: Set[Link]):
        self._uses_execution_environment = value

    @property
    @oslc_name("futureAction")
    @oslc_property_definition(NS_OSLC_AUTO["futureAction"])
    @oslc_description("A resource representing actions that will become available on Automation Results that result from execution of this Plan.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def future_action(self):
        return self._future_action

    @future_action.setter
    def future_action(self, value: Set[Link]):
        self._future_action = value
