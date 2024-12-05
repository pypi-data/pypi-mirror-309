from oslc4py_client.OSLCResource import OSLCResource
from oslc4py_client.annotation_types.Occurs import Occurs
from oslc4py_client.annotation_types.ValueType import ValueType
from oslc4py_client.decorators import oslc_description, oslc_name, oslc_namespace, oslc_occurs, oslc_property_definition, oslc_range, oslc_read_only, oslc_resource_shape, oslc_value_type
from oslc4py_domains_auto.oslc_constants import NS_DCTERMS, NS_FOAF, NS_OSLC, NS_OSLC_AUTO, NS_RDF, VERIFIT_UNIVERSAL_ANALYSIS
from datetime import datetime

@oslc_namespace(NS_OSLC_AUTO)
@oslc_name("Contribution")
@oslc_resource_shape(describes=NS_OSLC_AUTO["Contribution"], title="Contribution Resource Shape")
class Contribution(OSLCResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._title = None
        self._description = None
        self._type = set()
        self._value = None
        self._created = None
        self._value_type = set()
        self._creator = set()
        self._modified = None
        self._file_path = None

    @property
    @oslc_name("title")
    @oslc_property_definition(NS_DCTERMS["title"])
    @oslc_description("Title of the resource represented as rich text in XHTML content. SHOULD include only content that is valid inside an XHTML <span> element.")
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.XMLLITERAL)
    @oslc_read_only(False)
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    # Description property
    @property
    @oslc_name("description")
    @oslc_property_definition(NS_DCTERMS["description"])
    @oslc_description("Descriptive text about resource represented as rich text in XHTML content. SHOULD include only valid content for an XHTML <div> element.")
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.XMLLITERAL)
    @oslc_read_only(False)
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    #Type property (set of Links)
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
    
    def add_type(self, link):
        self._type.add(link)

    # Value property
    @property
    @oslc_name("value")
    @oslc_property_definition(NS_RDF["value"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.STRING)
    @oslc_read_only(False)
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    # Created property
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

    # ValueType property (set of Links)
    @property
    @oslc_name("valueType")
    @oslc_property_definition(NS_OSLC["valueType"])
    @oslc_description("List of allowed values for oslc:valueType. If omitted, the value type is unconstrained.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_read_only(False)
    def value_type(self):
        return self._value_type

    @value_type.setter
    def value_type(self, value: datetime):
        self._value_type = value

    def add_value_type(self, link):
        self._value_type.add(link)

    # Creator property (set of Links)
    @property
    @oslc_name("creator")
    @oslc_property_definition(NS_DCTERMS["creator"])
    @oslc_description("Creator of the resource, likely a foaf:Person but not necessarily.")
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_range(NS_FOAF["Person"])
    @oslc_read_only(False)
    def creator(self):
        return self._creator

    @creator.setter
    def creator(self, value: datetime):
        self._creator = value

    def add_creator(self, link):
        self._creator.add(link)

    # Modified property
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

    # FilePath property
    @property
    @oslc_name("filePath")
    @oslc_property_definition(VERIFIT_UNIVERSAL_ANALYSIS["filePath"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.STRING)
    @oslc_read_only(False)
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value: str):
        self._file_path = value

    # String representation (__str__)
    def __str__(self):
        result = ""
        if self._title:
            result += f"--title={self._title}<br>"
        if self._created:
            result += f"--created={self._created}<br>"
        if self._modified:
            result += f"--modified={self._modified}<br>"
        if self._creator:
            result += f"--creator={self._creator}<br>"
        if self._description:
            result += f"--description={self._description}<br>"
        if self._value:
            result += f"--value={self._value}<br>"
        if self._value_type:
            result += f"--valueType={list(self._value_type)[0]}<br>"
        if self._file_path:
            result += f"--filePath={self._file_path}<br>"
        if self._type:
            result += f"--type={list(self._type)[0]}<br>"
        return result or str(self.about)
