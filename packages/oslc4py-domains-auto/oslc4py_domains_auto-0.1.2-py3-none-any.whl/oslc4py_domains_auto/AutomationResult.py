from datetime import datetime
from typing import Set
from oslc4py_client.Link import Link
from oslc4py_client.OSLCResource import OSLCResource
from oslc4py_client.annotation_types.Occurs import Occurs
from oslc4py_client.annotation_types.Representation import Representation
from oslc4py_client.annotation_types.ValueType import ValueType
from oslc4py_client.decorators import oslc_description, oslc_name, oslc_namespace, oslc_occurs, oslc_property_definition, oslc_range, oslc_read_only, oslc_representation, oslc_resource_shape, oslc_value_type
from oslc4py_domains_auto.oslc_constants import NS_DCTERMS, NS_FOAF, NS_OSLC, NS_OSLC_AUTO, NS_RDF

@oslc_namespace(NS_OSLC_AUTO)
@oslc_name("AutomationResult")
@oslc_resource_shape(describes=NS_OSLC_AUTO["AutomationResult"], title="AutomationResult Resource Shape")
class AutomationResult(OSLCResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._identifier = None
        self._title = None
        self._contributor = set()
        self._created = None
        self._creator = set()
        self._modified = None
        self._type = set()
        self._subject = set()
        self._instance_shape = set()
        self._service_provider = set()
        self._state = set()
        self._desired_state = set()
        self._verdict = set()
        self._contribution = set()
        self._input_parameter = set()
        self._output_parameter = set()
        self._produced_by_automation_request = None
        self._reports_on_automation_plan = None
        self._created_sut = None
        
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
    def type(self, value):
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
    @oslc_representation(Representation.REFERENCE)
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
    @oslc_name("state")
    @oslc_property_definition(NS_OSLC_AUTO["state"])
    @oslc_description("The current state of the automation result.")
    @oslc_occurs(Occurs.ONE_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def state(self):
        return self._state

    @state.setter
    def state(self, value: Set[str]):
        self._state = value

    @property
    @oslc_name("desiredState")
    @oslc_property_definition(NS_OSLC_AUTO["desiredState"])
    @oslc_description("The desired state of the automation result.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def desired_state(self):
        return self._desired_state

    @desired_state.setter
    def desired_state(self, value: Set[str]):
        self._desired_state = value

    @property
    @oslc_name("verdict")
    @oslc_property_definition(NS_OSLC_AUTO["verdict"])
    @oslc_description("The verdict or outcome of the automation result.")
    @oslc_occurs(Occurs.ONE_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def verdict(self):
        return self._verdict

    @verdict.setter
    def verdict(self, value):
        self._verdict = value

    @property
    @oslc_name("contribution")
    @oslc_property_definition(NS_OSLC_AUTO["contribution"])
    @oslc_description("Contribution details related to the automation result.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.LOCALRESOURCE)
    @oslc_range(NS_OSLC_AUTO["Contribution"])
    @oslc_read_only(False)
    def contribution(self):
        return self._contribution

    @contribution.setter
    def contribution(self, value: Set[str]):
        self._contribution = value

    @property
    @oslc_name("inputParameter")
    @oslc_property_definition(NS_OSLC_AUTO["inputParameter"])
    @oslc_description("Input parameters for the automation result.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.LOCALRESOURCE)
    @oslc_range(NS_OSLC_AUTO["ParameterInstance"])
    @oslc_read_only(False)
    def input_parameter(self):
        return self._input_parameter

    @input_parameter.setter
    def input_parameter(self, value: Set[Link]):
        self._input_parameter = value

    @property
    @oslc_name("outputParameter")
    @oslc_property_definition(NS_OSLC_AUTO["outputParameter"])
    @oslc_description("Output parameters for the automation result.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.LOCALRESOURCE)
    @oslc_range(NS_OSLC_AUTO["ParameterInstance"])
    @oslc_read_only(False)
    def output_parameter(self):
        return self._output_parameter

    @output_parameter.setter
    def output_parameter(self, value: Set[Link]):
        self._output_parameter = value

    @property
    @oslc_name("producedByAutomationRequest")
    @oslc_property_definition(NS_OSLC_AUTO["producedByAutomationRequest"])
    @oslc_description("Link to the automation request that produced this result.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def produced_by_automation_request(self):
        return self._produced_by_automation_request

    @produced_by_automation_request.setter
    def produced_by_automation_request(self, value: Link):
        self._produced_by_automation_request = value

    @property
    @oslc_name("reportsOnAutomationPlan")
    @oslc_property_definition(NS_OSLC_AUTO["reportsOnAutomationPlan"])
    @oslc_description("Link to the automation plan this result reports on.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def reports_on_automation_plan(self):
        return self._reports_on_automation_plan

    @reports_on_automation_plan.setter
    def reports_on_automation_plan(self, value: Link):
        self._reports_on_automation_plan = value

    @property
    @oslc_name("createdSUT")
    @oslc_property_definition(NS_OSLC_AUTO["createdSUT"])
    @oslc_description("Link to the created System Under Test (SUT).")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.LOCALRESOURCE)
    @oslc_range(NS_OSLC_AUTO["SUT"])
    @oslc_read_only(False)
    def created_sut(self):
        return self._created_sut

    @created_sut.setter
    def created_sut(self, value: Link):
        self._created_sut = value