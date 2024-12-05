"""
Type annotations for elastic-inference service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_elastic_inference.client import ElasticInferenceClient

    session = Session()
    client: ElasticInferenceClient = session.client("elastic-inference")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .paginator import DescribeAcceleratorsPaginator
from .type_defs import (
    DescribeAcceleratorOfferingsRequestRequestTypeDef,
    DescribeAcceleratorOfferingsResponseTypeDef,
    DescribeAcceleratorsRequestRequestTypeDef,
    DescribeAcceleratorsResponseTypeDef,
    DescribeAcceleratorTypesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResultTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ElasticInferenceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class ElasticInferenceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticInferenceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.exceptions)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.can_paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.close)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#close)
        """

    def describe_accelerator_offerings(
        self, **kwargs: Unpack[DescribeAcceleratorOfferingsRequestRequestTypeDef]
    ) -> DescribeAcceleratorOfferingsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.describe_accelerator_offerings)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#describe_accelerator_offerings)
        """

    def describe_accelerator_types(self) -> DescribeAcceleratorTypesResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.describe_accelerator_types)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#describe_accelerator_types)
        """

    def describe_accelerators(
        self, **kwargs: Unpack[DescribeAcceleratorsRequestRequestTypeDef]
    ) -> DescribeAcceleratorsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.describe_accelerators)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#describe_accelerators)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.generate_presigned_url)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#generate_presigned_url)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.list_tags_for_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.tag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.untag_resource)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#untag_resource)
        """

    def get_paginator(
        self, operation_name: Literal["describe_accelerators"]
    ) -> DescribeAcceleratorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html#ElasticInference.Client.get_paginator)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastic_inference/client/#get_paginator)
        """
