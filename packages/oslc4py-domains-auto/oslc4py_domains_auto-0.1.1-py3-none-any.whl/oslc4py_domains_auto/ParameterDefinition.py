from typing import Set
from oslc4py_client.OSLCResource import OSLCResource
from oslc4py_client.annotation_types.Occurs import Occurs
from oslc4py_client.annotation_types.ValueType import ValueType
from oslc4py_client.decorators import oslc_description, oslc_name, oslc_namespace, oslc_occurs, oslc_property_definition, oslc_resource_shape, oslc_value_type, oslc_range, oslc_read_only
from oslc4py_domains_auto.oslc_constants import NS_DCTERMS, NS_OSLC, NS_OSLC_AUTO, VERIFIT_UNIVERSAL_ANALYSIS

@oslc_namespace(NS_OSLC_AUTO)
@oslc_name("ParameterDefinition")
@oslc_resource_shape(describes=NS_OSLC_AUTO["ParameterDefinition"], title="ParameterDefinition Resource Shape")
class ParameterDefinition(OSLCResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._description = None
        self._title = None
        self._allowed_value = set()
        self._default_value = None
        self._allowed_values = None
        self._hidden = None
        self._is_member_property = None
        self._name = None
        self._max_size = None
        self._occurs = None
        self._range = set()
        self._read_only = None
        self._representation = None
        self._value_type = set()
        self._value_shape = None
        self._commandline_position = None
        self._property_definition = None
        self._value_prefix = None

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
    @oslc_name("title")
    @oslc_property_definition(NS_DCTERMS["title"])
    @oslc_description("Title of the resource.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.STRING)
    @oslc_read_only(False)
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    @property
    @oslc_name("allowedValue")
    @oslc_property_definition(NS_OSLC["allowedValue"])
    @oslc_description("value allowed for a property")
    @oslc_occurs(Occurs.ONE_OR_MANY)
    @oslc_value_type("string")
    @oslc_read_only(False)
    def allowed_value(self):
        return self._allowed_value

    @allowed_value.setter
    def allowed_value(self, value: Set[str]):
        self._allowed_value = value

    @property
    @oslc_name("defaultValue")
    @oslc_property_definition(NS_OSLC["defaultValue"])
    @oslc_description("A default value for property, inlined into property definition.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type("string")
    @oslc_read_only(False)
    def default_value(self):
        return self._default_value

    @default_value.setter
    def default_value(self, value: str):
        self._default_value = value

    @property
    @oslc_name("allowedValues")
    @oslc_property_definition(NS_OSLC["allowedValues"])
    @oslc_description("Resource with allowed values for the property being defined.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def allowed_values(self):
        return self._allowed_values

    @allowed_values.setter
    def allowed_values(self, value):
        self._allowed_values = value

    @property
    @oslc_name("hidden")
    @oslc_property_definition(NS_OSLC["hidden"])
    @oslc_description("A hint that indicates that property MAY be hidden when presented in a user interface.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type("boolean")
    @oslc_read_only(False)
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, value: bool):
        self._hidden = value

    @property
    @oslc_name("isMemberProperty")
    @oslc_property_definition(NS_OSLC["isMemberProperty"])
    @oslc_description("If set to true, this indicates that the property is a membership property.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type("boolean")
    @oslc_read_only(False)
    def is_member_property(self):
        return self._is_member_property

    @is_member_property.setter
    def is_member_property(self, value: bool):
        self._is_member_property = value

    @property
    @oslc_name("name")
    @oslc_property_definition(NS_OSLC["name"])
    @oslc_description("Name of property being defined.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type("string")
    @oslc_read_only(False)
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    @oslc_name("maxSize")
    @oslc_property_definition(NS_OSLC["maxSize"])
    @oslc_description("For String properties only, specifies maximum characters allowed.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type("integer")
    @oslc_read_only(False)
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, value: int):
        self._max_size = value

    @property
    @oslc_name("occurs")
    @oslc_property_definition(NS_OSLC["occurs"])
    @oslc_description("Specifies how many times the property can occur.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def occurs(self):
        return self._occurs

    @occurs.setter
    def occurs(self, value):
        self._occurs = value

    @property
    @oslc_name("range")
    @oslc_property_definition(NS_OSLC["range"])
    @oslc_description("Specifies the range of possible resource types allowed.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        self._range = value

    @property
    @oslc_name("readOnly")
    @oslc_property_definition(NS_OSLC["readOnly"])
    @oslc_description("true if the property is read-only.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type("boolean")
    @oslc_read_only(False)
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, value: bool):
        self._read_only = value

    @property
    @oslc_name("representation")
    @oslc_property_definition(NS_OSLC["representation"])
    @oslc_description("Specifies how the property should be represented.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def representation(self):
        return self._representation

    @representation.setter
    def representation(self, value):
        self._representation = value

    @property
    @oslc_name("valueType")
    @oslc_property_definition(NS_OSLC["valueType"])
    @oslc_description("Specifies the value type of the property.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def value_type(self):
        return self._value_type

    @value_type.setter
    def value_type(self, value):
        self._value_type = value

    @property
    @oslc_name("valueShape")
    @oslc_property_definition(NS_OSLC["valueShape"])
    @oslc_description("Specifies the Resource Shape that applies to the resource.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def value_shape(self):
        return self._value_shape

    @value_shape.setter
    def value_shape(self, value):
        self._value_shape = value

    @property
    @oslc_name("commandlinePosition")
    @oslc_property_definition(VERIFIT_UNIVERSAL_ANALYSIS["commandlinePosition"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type("integer")
    @oslc_read_only(False)
    def commandline_position(self):
        return self._commandline_position
    
    @commandline_position.setter
    def commandlinePosition(self, value: int) -> None:
        self._commandline_position = value

    @property
    @oslc_name("propertyDefinition")
    @oslc_property_definition(VERIFIT_UNIVERSAL_ANALYSIS["propertyDefinition"])
    @oslc_description("Property definitions.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.LOCALRESOURCE)
    @oslc_read_only(False)
    def property_definition(self) -> set:
        return self._property_definition

    @property_definition.setter
    def property_definition(self, value: set) -> None:
        self._property_definition = value

    @property
    @oslc_name("valuePrefix")
    @oslc_property_definition(VERIFIT_UNIVERSAL_ANALYSIS["valuePrefix"])
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    def value_prefix(self) -> None:
        return self._value_prefix

    @value_prefix.setter
    def value_prefix(self, value: None) -> None:
        self._value_prefix = value