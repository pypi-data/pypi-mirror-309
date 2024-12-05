"""
Type annotations for glacier service ServiceResource

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_glacier.service_resource import GlacierServiceResource
    import mypy_boto3_glacier.service_resource as glacier_resources

    session = Session()
    resource: GlacierServiceResource = session.resource("glacier")

    my_account: glacier_resources.Account = resource.Account(...)
    my_archive: glacier_resources.Archive = resource.Archive(...)
    my_job: glacier_resources.Job = resource.Job(...)
    my_multipart_upload: glacier_resources.MultipartUpload = resource.MultipartUpload(...)
    my_notification: glacier_resources.Notification = resource.Notification(...)
    my_vault: glacier_resources.Vault = resource.Vault(...)
```
"""

import sys
from typing import Iterator, List, Sequence

from boto3.resources.base import ResourceMeta, ServiceResource
from boto3.resources.collection import ResourceCollection

from .client import GlacierClient
from .literals import ActionCodeType, StatusCodeType
from .type_defs import (
    ArchiveCreationOutputTypeDef,
    CompleteMultipartUploadInputMultipartUploadCompleteTypeDef,
    CreateVaultInputAccountCreateVaultTypeDef,
    CreateVaultInputServiceResourceCreateVaultTypeDef,
    CreateVaultOutputTypeDef,
    GetJobOutputInputJobGetOutputTypeDef,
    GetJobOutputOutputTypeDef,
    InitiateMultipartUploadInputVaultInitiateMultipartUploadTypeDef,
    InventoryRetrievalJobDescriptionTypeDef,
    ListPartsInputMultipartUploadPartsTypeDef,
    ListPartsOutputTypeDef,
    OutputLocationOutputTypeDef,
    SelectParametersTypeDef,
    SetVaultNotificationsInputNotificationSetTypeDef,
    UploadArchiveInputVaultUploadArchiveTypeDef,
    UploadMultipartPartInputMultipartUploadUploadPartTypeDef,
    UploadMultipartPartOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "Account",
    "AccountVaultsCollection",
    "Archive",
    "GlacierServiceResource",
    "Job",
    "MultipartUpload",
    "Notification",
    "ServiceResourceVaultsCollection",
    "Vault",
    "VaultCompletedJobsCollection",
    "VaultFailedJobsCollection",
    "VaultJobsCollection",
    "VaultJobsInProgressCollection",
    "VaultMultipartUplaodsCollection",
    "VaultMultipartUploadsCollection",
    "VaultSucceededJobsCollection",
)

class ServiceResourceVaultsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#serviceresourcevaultscollection)
    """
    def all(self) -> "ServiceResourceVaultsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

    def filter(  # type: ignore
        self, *, marker: str = ..., limit: str = ...
    ) -> "ServiceResourceVaultsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

    def limit(self, count: int) -> "ServiceResourceVaultsCollection":
        """
        Return at most this many Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceVaultsCollection":
        """
        Fetch at most this many Vaults per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

    def pages(self) -> Iterator[List["Vault"]]:
        """
        A generator which yields pages of Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

    def __iter__(self) -> Iterator["Vault"]:
        """
        A generator which yields Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

class AccountVaultsCollection(ResourceCollection):
    def all(self) -> "AccountVaultsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, marker: str = ..., limit: str = ...
    ) -> "AccountVaultsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "AccountVaultsCollection":
        """
        Return at most this many Vaults.
        """

    def page_size(self, count: int) -> "AccountVaultsCollection":
        """
        Fetch at most this many Vaults per service request.
        """

    def pages(self) -> Iterator[List["Vault"]]:
        """
        A generator which yields pages of Vaults.
        """

    def __iter__(self) -> Iterator["Vault"]:
        """
        A generator which yields Vaults.
        """

class VaultCompletedJobsCollection(ResourceCollection):
    def all(self) -> "VaultCompletedJobsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> "VaultCompletedJobsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VaultCompletedJobsCollection":
        """
        Return at most this many Jobs.
        """

    def page_size(self, count: int) -> "VaultCompletedJobsCollection":
        """
        Fetch at most this many Jobs per service request.
        """

    def pages(self) -> Iterator[List["Job"]]:
        """
        A generator which yields pages of Jobs.
        """

    def __iter__(self) -> Iterator["Job"]:
        """
        A generator which yields Jobs.
        """

class VaultFailedJobsCollection(ResourceCollection):
    def all(self) -> "VaultFailedJobsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> "VaultFailedJobsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VaultFailedJobsCollection":
        """
        Return at most this many Jobs.
        """

    def page_size(self, count: int) -> "VaultFailedJobsCollection":
        """
        Fetch at most this many Jobs per service request.
        """

    def pages(self) -> Iterator[List["Job"]]:
        """
        A generator which yields pages of Jobs.
        """

    def __iter__(self) -> Iterator["Job"]:
        """
        A generator which yields Jobs.
        """

class VaultJobsCollection(ResourceCollection):
    def all(self) -> "VaultJobsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> "VaultJobsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VaultJobsCollection":
        """
        Return at most this many Jobs.
        """

    def page_size(self, count: int) -> "VaultJobsCollection":
        """
        Fetch at most this many Jobs per service request.
        """

    def pages(self) -> Iterator[List["Job"]]:
        """
        A generator which yields pages of Jobs.
        """

    def __iter__(self) -> Iterator["Job"]:
        """
        A generator which yields Jobs.
        """

class VaultJobsInProgressCollection(ResourceCollection):
    def all(self) -> "VaultJobsInProgressCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> "VaultJobsInProgressCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VaultJobsInProgressCollection":
        """
        Return at most this many Jobs.
        """

    def page_size(self, count: int) -> "VaultJobsInProgressCollection":
        """
        Fetch at most this many Jobs per service request.
        """

    def pages(self) -> Iterator[List["Job"]]:
        """
        A generator which yields pages of Jobs.
        """

    def __iter__(self) -> Iterator["Job"]:
        """
        A generator which yields Jobs.
        """

class VaultMultipartUplaodsCollection(ResourceCollection):
    def all(self) -> "VaultMultipartUplaodsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, marker: str = ..., limit: str = ...
    ) -> "VaultMultipartUplaodsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VaultMultipartUplaodsCollection":
        """
        Return at most this many MultipartUploads.
        """

    def page_size(self, count: int) -> "VaultMultipartUplaodsCollection":
        """
        Fetch at most this many MultipartUploads per service request.
        """

    def pages(self) -> Iterator[List["MultipartUpload"]]:
        """
        A generator which yields pages of MultipartUploads.
        """

    def __iter__(self) -> Iterator["MultipartUpload"]:
        """
        A generator which yields MultipartUploads.
        """

class VaultMultipartUploadsCollection(ResourceCollection):
    def all(self) -> "VaultMultipartUploadsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, marker: str = ..., limit: str = ...
    ) -> "VaultMultipartUploadsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VaultMultipartUploadsCollection":
        """
        Return at most this many MultipartUploads.
        """

    def page_size(self, count: int) -> "VaultMultipartUploadsCollection":
        """
        Fetch at most this many MultipartUploads per service request.
        """

    def pages(self) -> Iterator[List["MultipartUpload"]]:
        """
        A generator which yields pages of MultipartUploads.
        """

    def __iter__(self) -> Iterator["MultipartUpload"]:
        """
        A generator which yields MultipartUploads.
        """

class VaultSucceededJobsCollection(ResourceCollection):
    def all(self) -> "VaultSucceededJobsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> "VaultSucceededJobsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VaultSucceededJobsCollection":
        """
        Return at most this many Jobs.
        """

    def page_size(self, count: int) -> "VaultSucceededJobsCollection":
        """
        Fetch at most this many Jobs per service request.
        """

    def pages(self) -> Iterator[List["Job"]]:
        """
        A generator which yields pages of Jobs.
        """

    def __iter__(self) -> Iterator["Job"]:
        """
        A generator which yields Jobs.
        """

class Account(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Account)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#account)
    """

    id: str
    vaults: AccountVaultsCollection
    meta: "GlacierResourceMeta"  # type: ignore

    def Vault(self, name: str) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Account.Vault)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#accountvault-method)
        """

    def create_vault(self, **kwargs: Unpack[CreateVaultInputAccountCreateVaultTypeDef]) -> "_Vault":
        """
        This operation creates a new vault with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Account.create_vault)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#accountcreate_vault-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Account.get_available_subresources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#accountget_available_subresources-method)
        """

_Account = Account

class Job(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Job)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#job)
    """

    job_id: str
    job_description: str
    action: ActionCodeType
    archive_id: str
    vault_arn: str
    creation_date: str
    completed: bool
    status_code: StatusCodeType
    status_message: str
    archive_size_in_bytes: int
    inventory_size_in_bytes: int
    sns_topic: str
    completion_date: str
    sha256_tree_hash: str
    archive_sha256_tree_hash: str
    retrieval_byte_range: str
    tier: str
    inventory_retrieval_parameters: InventoryRetrievalJobDescriptionTypeDef
    job_output_path: str
    select_parameters: SelectParametersTypeDef
    output_location: OutputLocationOutputTypeDef
    account_id: str
    vault_name: str
    id: str
    meta: "GlacierResourceMeta"  # type: ignore

    def Vault(self) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Job.Vault)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#jobvault-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Job.get_available_subresources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#jobget_available_subresources-method)
        """

    def get_output(
        self, **kwargs: Unpack[GetJobOutputInputJobGetOutputTypeDef]
    ) -> GetJobOutputOutputTypeDef:
        """
        This operation downloads the output of the job you initiated using  InitiateJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Job.get_output)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#jobget_output-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.describe_job` to update the attributes of the
        Job
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Job.load)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#jobload-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.describe_job` to update the attributes of the
        Job
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Job.reload)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#jobreload-method)
        """

_Job = Job

class MultipartUpload(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.MultipartUpload)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#multipartupload)
    """

    multipart_upload_id: str
    vault_arn: str
    archive_description: str
    part_size_in_bytes: int
    creation_date: str
    account_id: str
    vault_name: str
    id: str
    meta: "GlacierResourceMeta"  # type: ignore

    def Vault(self) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.Vault)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#multipartuploadvault-method)
        """

    def abort(self) -> None:
        """
        This operation aborts a multipart upload identified by the upload ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.abort)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#multipartuploadabort-method)
        """

    def complete(
        self, **kwargs: Unpack[CompleteMultipartUploadInputMultipartUploadCompleteTypeDef]
    ) -> ArchiveCreationOutputTypeDef:
        """
        You call this operation to inform Amazon S3 Glacier (Glacier) that all the
        archive parts have been uploaded and that Glacier can now assemble the archive
        from the uploaded
        parts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.complete)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#multipartuploadcomplete-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.get_available_subresources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#multipartuploadget_available_subresources-method)
        """

    def parts(
        self, **kwargs: Unpack[ListPartsInputMultipartUploadPartsTypeDef]
    ) -> ListPartsOutputTypeDef:
        """
        This operation lists the parts of an archive that have been uploaded in a
        specific multipart
        upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.parts)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#multipartuploadparts-method)
        """

    def upload_part(
        self, **kwargs: Unpack[UploadMultipartPartInputMultipartUploadUploadPartTypeDef]
    ) -> UploadMultipartPartOutputTypeDef:
        """
        This operation uploads a part of an archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.upload_part)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#multipartuploadupload_part-method)
        """

_MultipartUpload = MultipartUpload

class Notification(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Notification)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#notification)
    """

    sns_topic: str
    events: List[str]
    account_id: str
    vault_name: str
    meta: "GlacierResourceMeta"  # type: ignore

    def Vault(self) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.Vault)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#notificationvault-method)
        """

    def delete(self) -> None:
        """
        This operation deletes the notification configuration set for a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.delete)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#notificationdelete-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.get_available_subresources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#notificationget_available_subresources-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.get_vault_notifications` to update the
        attributes of the Notification
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.load)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#notificationload-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.get_vault_notifications` to update the
        attributes of the Notification
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.reload)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#notificationreload-method)
        """

    def set(self, **kwargs: Unpack[SetVaultNotificationsInputNotificationSetTypeDef]) -> None:
        """
        This operation configures notifications that will be sent when specific events
        happen to a
        vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.set)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#notificationset-method)
        """

_Notification = Notification

class Archive(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Archive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#archive)
    """

    account_id: str
    vault_name: str
    id: str
    meta: "GlacierResourceMeta"  # type: ignore

    def Vault(self) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Archive.Vault)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#archivevault-method)
        """

    def delete(self) -> None:
        """
        This operation deletes an archive from a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Archive.delete)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#archivedelete-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Archive.get_available_subresources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#archiveget_available_subresources-method)
        """

    def initiate_archive_retrieval(self) -> "_Job":
        """
        This operation initiates a job of the specified type, which can be a select, an
        archival retrieval, or a vault
        retrieval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Archive.initiate_archive_retrieval)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#archiveinitiate_archive_retrieval-method)
        """

_Archive = Archive

class Vault(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Vault)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vault)
    """

    vault_arn: str
    vault_name: str
    creation_date: str
    last_inventory_date: str
    number_of_archives: int
    size_in_bytes: int
    account_id: str
    name: str
    completed_jobs: VaultCompletedJobsCollection
    failed_jobs: VaultFailedJobsCollection
    jobs: VaultJobsCollection
    jobs_in_progress: VaultJobsInProgressCollection
    multipart_uplaods: VaultMultipartUplaodsCollection
    multipart_uploads: VaultMultipartUploadsCollection
    succeeded_jobs: VaultSucceededJobsCollection
    meta: "GlacierResourceMeta"  # type: ignore

    def Account(self) -> "_Account":
        """
        Creates a Account resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.Account)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultaccount-method)
        """

    def Archive(self, id: str) -> "_Archive":
        """
        Creates a Archive resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.Archive)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultarchive-method)
        """

    def Job(self, id: str) -> "_Job":
        """
        Creates a Job resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.Job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultjob-method)
        """

    def MultipartUpload(self, id: str) -> "_MultipartUpload":
        """
        Creates a MultipartUpload resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.MultipartUpload)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultmultipartupload-method)
        """

    def Notification(self) -> "_Notification":
        """
        Creates a Notification resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.Notification)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultnotification-method)
        """

    def create(self) -> CreateVaultOutputTypeDef:
        """
        This operation creates a new vault with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.create)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultcreate-method)
        """

    def delete(self) -> None:
        """
        This operation deletes a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.delete)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultdelete-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.get_available_subresources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultget_available_subresources-method)
        """

    def initiate_inventory_retrieval(self) -> "_Job":
        """
        This operation initiates a job of the specified type, which can be a select, an
        archival retrieval, or a vault
        retrieval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.initiate_inventory_retrieval)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultinitiate_inventory_retrieval-method)
        """

    def initiate_multipart_upload(
        self, **kwargs: Unpack[InitiateMultipartUploadInputVaultInitiateMultipartUploadTypeDef]
    ) -> "_MultipartUpload":
        """
        This operation initiates a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.initiate_multipart_upload)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultinitiate_multipart_upload-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.describe_vault` to update the attributes of the
        Vault
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.load)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultload-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.describe_vault` to update the attributes of the
        Vault
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.reload)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultreload-method)
        """

    def upload_archive(
        self, **kwargs: Unpack[UploadArchiveInputVaultUploadArchiveTypeDef]
    ) -> "_Archive":
        """
        This operation adds an archive to a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.upload_archive)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#vaultupload_archive-method)
        """

_Vault = Vault

class GlacierResourceMeta(ResourceMeta):
    client: GlacierClient

class GlacierServiceResource(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/)
    """

    meta: "GlacierResourceMeta"  # type: ignore
    vaults: ServiceResourceVaultsCollection

    def Account(self, id: str) -> "_Account":
        """
        Creates a Account resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Account)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#glacierserviceresourceaccount-method)
        """

    def Archive(self, account_id: str, vault_name: str, id: str) -> "_Archive":
        """
        Creates a Archive resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Archive)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#glacierserviceresourcearchive-method)
        """

    def Job(self, account_id: str, vault_name: str, id: str) -> "_Job":
        """
        Creates a Job resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Job)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#glacierserviceresourcejob-method)
        """

    def MultipartUpload(self, account_id: str, vault_name: str, id: str) -> "_MultipartUpload":
        """
        Creates a MultipartUpload resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.MultipartUpload)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#glacierserviceresourcemultipartupload-method)
        """

    def Notification(self, account_id: str, vault_name: str) -> "_Notification":
        """
        Creates a Notification resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Notification)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#glacierserviceresourcenotification-method)
        """

    def Vault(self, account_id: str, name: str) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Vault)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#glacierserviceresourcevault-method)
        """

    def create_vault(
        self, **kwargs: Unpack[CreateVaultInputServiceResourceCreateVaultTypeDef]
    ) -> "_Vault":
        """
        This operation creates a new vault with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.create_vault)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#glacierserviceresourcecreate_vault-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.get_available_subresources)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/service_resource/#glacierserviceresourceget_available_subresources-method)
        """
