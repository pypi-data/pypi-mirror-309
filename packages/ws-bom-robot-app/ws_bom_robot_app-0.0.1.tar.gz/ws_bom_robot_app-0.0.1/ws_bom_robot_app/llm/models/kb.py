import json, os , uuid, requests
from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, Field, AliasChoices
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.json_loader import JsonLoader
from ws_bom_robot_app.util import timer

class LlmKbIntegration(BaseModel):
  type: str = Field(..., validation_alias=AliasChoices("blockType","type"))
  class Config:
        extra = "allow"
  class ConfigDict:
        extra = "allow"

class ExternalEndpointAuthentication(str, Enum):
    NONE = 'none'
    BASIC = 'basic'
    BEARER = 'bearer'
    CUSTOM = 'custom'

class LlmKbEndpointFieldsMapping(BaseModel):
    class ReplacedField(BaseModel):
        src_name: str = Field(validation_alias=AliasChoices("srcName","src_name"))
        dest_name: str = Field(validation_alias=AliasChoices("destName","dest_name"))
    class NamedField(BaseModel):
        name: str
    class NewField(NamedField):
        value: str
    class MetaField(NamedField):
        description: str
        type: Literal['string',f'int',f'float',f'bool']
    replaced_fields: Optional[list[ReplacedField]] = Field(default_factory=list, validation_alias=AliasChoices("replacedFields","replaced_fields"))
    new_fields: Optional[list[NewField]] = Field(default_factory=list, validation_alias=AliasChoices("newFields","new_fields"))
    deleted_fields: Optional[list[NamedField]] = Field(default_factory=list, validation_alias=AliasChoices("deletedFields","deleted_fields"))
    """ select fields to be included in the metadata of the document
    Sample:
    [
      { "name": "price", description": "Product price", "type": "float" },
      { "name": "qty", "description": "Product availabilty: number of sellable items", "type": "int" }
    ]
    """
    meta_fields: Optional[list[MetaField]] = Field(default_factory=list, validation_alias=AliasChoices("metaFields","meta_fields"))

class LlmKbEndpoint(BaseModel):
    endpoint_url: str = Field(validation_alias=AliasChoices("endpointUrl","endpoint_url"))
    authentication: ExternalEndpointAuthentication
    auth_secret: str = Field(validation_alias=AliasChoices("authSecret","auth_secret"))
    fields_mapping: LlmKbEndpointFieldsMapping = Field(validation_alias=AliasChoices("fieldsMapping","fields_mapping"))

# Remapping Function
def __remap_knowledgebase_file(filepath: str, mapping: LlmKbEndpointFieldsMapping) -> None:
    map_new_fields = mapping.new_fields or []
    map_replaced_fields = mapping.replaced_fields or []
    deleted_fields = mapping.deleted_fields or []

    if all([not map_new_fields,not map_replaced_fields,not deleted_fields]):
        return

    with open(filepath, 'r', encoding='utf8') as file:
        original_data = json.load(file)

    for item in original_data:
        # Replaced fields
        for field in map_replaced_fields:
            if '.' in field.src_name:
                keys = field.src_name.split('.')
                last_key = keys.pop()
                obj = item
                for key in keys:
                    obj = obj.get(key, None)
                if obj is not None:
                    obj[field.dest_name] = obj.pop(last_key, None)
            else:
                item[field.dest_name] = item.pop(field.src_name, None)

        # Deleted fields
        for field in deleted_fields:
            if '.' in field.name:
                keys = field.name.split('.')
                last_key = keys.pop()
                obj = item
                for key in keys:
                    obj = obj.get(key, None)
                if obj is not None:
                    obj.pop(last_key, None)
            else:
                item.pop(field.name, None)

        # New fields
        for field in map_new_fields:
            item[field.name] = field.value

    with open(filepath, 'w', encoding='utf8') as file:
        json.dump(original_data, file, ensure_ascii=False, indent=4)

# Download External Endpoints
@timer
def load_endpoints(endpoints: list[LlmKbEndpoint], destination_directory: str) -> list[Document]:
    _documents = []

    for endpoint in endpoints:
        headers = {}
        if endpoint.authentication != ExternalEndpointAuthentication.NONE:
          auth_formats = {
              ExternalEndpointAuthentication.BASIC: lambda secret: f'Basic {secret}',
              ExternalEndpointAuthentication.BEARER: lambda secret: f'Bearer {secret}',
              ExternalEndpointAuthentication.CUSTOM: lambda secret: secret
          }
          headers['Authorization'] = auth_formats[endpoint.authentication](endpoint.auth_secret)
        try:
          response = requests.get(endpoint.endpoint_url, headers=headers)
          response.raise_for_status()

          mime_type = response.headers.get('content-type', None)
          if mime_type == 'application/json':
              filename = f"{uuid.uuid4()}.json"
              file_path = os.path.join(destination_directory, filename)
              with open(file_path, 'wb') as file:
                  file.write(response.content)
              __remap_knowledgebase_file(file_path, endpoint.fields_mapping)
              _documents.extend(
                  JsonLoader(
                      file_path,
                      meta_fields=[field.name for field in endpoint.fields_mapping.meta_fields] if endpoint.fields_mapping.meta_fields else []
                      ).load())
          else:
              raise Exception(f"Unsupported content type {mime_type}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to download file from endpoint [status {response.status_code}]: {endpoint.endpoint_url}") from e

    return _documents

