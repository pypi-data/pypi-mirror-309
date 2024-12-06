from pydantic import BaseModel, ConfigDict, Field

from contextcheck.connectors.connector import ConnectorBase
from contextcheck.endpoints.endpoint_config import EndpointConfig
from contextcheck.models.request import RequestBase
from contextcheck.models.response import ResponseBase


class EndpointBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    connector: ConnectorBase = Field(
        default_factory=ConnectorBase,
        description="A connector responsible for connection to llm/rag",
    )
    config: EndpointConfig = Field(
        default_factory=EndpointConfig, description="Configuration for llm/rag"
    )

    class RequestModel(RequestBase):
        pass

    class ResponseModel(ResponseBase):
        pass

    def send_request(self, req: RequestBase) -> ResponseBase:
        req = self.RequestModel(**req.model_dump())
        with self.connector as c:
            response_dict = c.send(req.model_dump())
        response_dict.update({"config": self.config})
        response = self.ResponseModel.model_validate(response_dict)

        # Add connector stats to response stats:
        response.stats = response.stats.model_copy(update=c.stats.model_dump())

        return response
