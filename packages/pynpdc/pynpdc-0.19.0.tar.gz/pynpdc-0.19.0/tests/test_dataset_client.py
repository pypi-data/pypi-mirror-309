from datetime import datetime
import hashlib
import io
import os
import pytest
import shutil
import tempfile
from typing import Any, Dict, Optional
import unittest
from urllib.parse import urlencode
import urllib3
import uuid
import zipfile

from pynpdc.auth_client import AuthClient
from pynpdc.dataset_client import (
    DatasetClient,
)
from pynpdc.exception import (
    APIException,
    MissingAccountException,
    MissingClientException,
)
from pynpdc.models import (
    Attachment,
    AttachmentAPIResponse,
    AttachmentCollection,
    Dataset,
    DatasetAPIResponse,
    DatasetCollection,
    DatasetType,
    Permission,
    PermissionAPIResponse,
    PermissionCollection,
    Prefix,
    PrefixCollection,
    Record,
    RecordCollection,
    RecordCreationInfo,
    RecordCreateDTO,
    AttachmentCreateDTO,
    AttachmentCreationInfo,
    DEFAULT_CHUNK_SIZE,
)

from .helpers import create_invalid_test_auth, get_test_config

"""
Prerequisites for this test suite:
- a user foo@example.org with password 1234123412341234 has to exist in auth
- another user internal@npolar.no with ID ae968c1d-a133-4dce-9fd1-a582f7c8c841 has
  to exist in auth
- at least one public dataset with id PUBLIC_ID has to exist
- the public dataset must have one file, that is not too large to avoid
  performance issues in the test

When testing a nullable object for being not null, a special pattern is used to
make mypy pass when object properties are accessed.

bad:

self.assertIsInstance(dataset, Dataset)

good:

self.assertIsInstance(dataset, Dataset)
if type(dataset) is not Dataset:  # make mypy happy
    raise Exception()

"""


class FixtureProperties:
    anonymous_client: DatasetClient
    authorized_client: DatasetClient
    authorized_user_id: uuid.UUID
    invalid_token_client: DatasetClient
    tag: str
    DRAFT_ID: uuid.UUID
    PUBLIC_ID: uuid.UUID
    OTHER_USER_ID: uuid.UUID


class FixtureType:
    cls: FixtureProperties


@pytest.fixture(scope="class")
def run_fixtures(request: FixtureType) -> None:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # config
    cfg = get_test_config()

    # anonymous_client
    request.cls.anonymous_client = DatasetClient(cfg.kinko.entrypoint, verify_ssl=False)

    # authorized_client
    auth_client = AuthClient(cfg.komainu.entrypoint, verify_ssl=False)
    account = auth_client.login(cfg.komainu.test_user, cfg.komainu.test_password)
    request.cls.authorized_client = DatasetClient(
        cfg.kinko.entrypoint, auth=account, verify_ssl=False
    )
    request.cls.authorized_user_id = account.id

    # client with invalid token
    auth = create_invalid_test_auth()
    request.cls.invalid_token_client = DatasetClient(
        cfg.kinko.entrypoint, auth=auth, verify_ssl=False
    )

    # tag
    request.cls.tag = cfg.kinko.summary_tag

    # cleanup of previous run
    for dataset in request.cls.authorized_client.get_datasets(q=request.cls.tag):
        if dataset.type == DatasetType.DRAFT:
            request.cls.authorized_client.delete_dataset(dataset.id)

    # draft dataset
    content = {
        "title": "unittest draft dataset #pynpdcdraft",
        "summary": request.cls.tag,
    }
    dataset = request.cls.authorized_client.create_dataset(content)
    request.cls.DRAFT_ID = dataset.id

    # public dataset
    request.cls.PUBLIC_ID = cfg.kinko.public_id

    # other user (for Account tests)
    request.cls.OTHER_USER_ID = cfg.komainu.other_user_id


class FixtureMethods(unittest.TestCase, FixtureProperties):

    def _create_draft(
        self,
        title: str = "Draft dataset",
    ) -> uuid.UUID:
        content = dict(title=f"[pynpdc unit test] {title}", summary=self.tag)
        dataset = self.authorized_client.create_dataset(content)
        self.assertIsInstance(dataset, Dataset)
        return dataset.id

    def _create_attachment(
        self,
        dataset_id: uuid.UUID,
        content: bytes,
        filename: str = "test.txt",
        *,
        mime_type: str = "text/plain",
    ) -> uuid.UUID:
        dto = AttachmentCreateDTO(io.BytesIO(content), filename, mime_type=mime_type)
        info = self.authorized_client.add_attachment(dataset_id, dto)
        return info.id

    def _create_record(
        self, dataset_id: uuid.UUID, values: Dict[str, Any] = {"mol": 42}
    ) -> uuid.UUID:
        # ⚠️ at time (2024-10-28) the API does not return the ID(s) of the
        #   created record(s). Therefore we build an own random ID and add it to
        #   the request (ID is optional there). So we do not rely on the
        #   response body providing the ID of the created record

        now = datetime.now().isoformat()
        record_id = uuid.uuid4()
        content = {
            "id": "test01@" + now,
            "measured": now,
            "values": [{"key": k, "value": v} for k, v in values.items()],
        }
        dto = RecordCreateDTO(id=record_id, content=content, type="measurement")

        self.authorized_client.add_record(dataset_id, dto)

        return record_id

    def _delete_records(self, dataset_id: uuid.UUID) -> None:
        for record in self.authorized_client.get_records(dataset_id):
            try:
                self.authorized_client.delete_record(dataset_id, record.id)
            except APIException as e:
                if e.status_code != 404:
                    raise e


@pytest.mark.usefixtures("run_fixtures")
class TestDataset(FixtureMethods):
    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Private methods

    def test_is_list_of_dicts(self) -> None:
        tests = [
            (3, False),
            ({"x": 1}, False),
            ([], True),
            ([3], False),
            ([{"x": 1}], True),
        ]

        for mixed, result in tests:
            self.assertEqual(self.anonymous_client._is_list_of_dicts(mixed), result)

    # Get API Version

    def test_get_api_version(self) -> None:
        v = self.anonymous_client.get_api_version()
        self.assertEqual(len(v), 8)

    # READ DATASET COLLECTION

    def test_get_datasets(self) -> None:
        title = "pynpdcmasscreate"
        total_num = 5
        for i in range(total_num):
            self._create_draft(f"{title} {i}")

        tests = [
            # query, num returned items, chunk_size of lazy collection
            (dict(q=title), 5, DEFAULT_CHUNK_SIZE),
            (dict(q=title), 5, 5),
            (dict(q=title), 5, 2),
            (dict(q=title), 5, 1),
            (dict(q=title, skip=3), 2, DEFAULT_CHUNK_SIZE),
            (dict(q=title, take=1), 1, DEFAULT_CHUNK_SIZE),
            (dict(q=title, take=4), 4, 3),
            (dict(q=title, skip=1, take=2), 2, 1),
        ]

        for query, item_num, chunk_size in tests:
            msg = urlencode(query)  # type:ignore
            gen = self.authorized_client.get_datasets(
                chunk_size=chunk_size, **query
            )  # type:ignore
            self.assertIsInstance(gen, DatasetCollection, msg)
            self.assertIsNone(gen.count)

            datasets = list(gen)
            self.assertGreaterEqual(len(datasets), item_num, msg)

        if item_num > 0:
            # check 1st item
            self.assertIsInstance(datasets[0], Dataset, msg)
            self.assertEqual(datasets[0].type, DatasetType.DRAFT, msg)

    def test_get_only_draft_datasets(self) -> None:
        self._create_draft("draftexample")

        datasets = list(self.authorized_client.get_datasets(type=DatasetType.DRAFT))
        self.assertGreater(len(datasets), 0)

        for dataset in datasets:
            self.assertEqual(dataset.type, DatasetType.DRAFT)

    def test_get_draft_datasets_with_count(self) -> None:
        self._create_draft("draftexample 1")
        self._create_draft("draftexample 2")

        gen = self.authorized_client.get_datasets(
            type=DatasetType.DRAFT, take=1, count=True
        )
        datasets = list(gen)

        self.assertGreaterEqual(len(datasets), 1)

        self.assertIsInstance(gen.count, int)
        if type(gen.count) is not int:  # make mypy happy
            raise Exception()
        self.assertGreaterEqual(gen.count, 2)

    def test_get_datasets_by_iterator(self) -> None:
        self._create_draft("pynpdciterator 1")
        self._create_draft("pynpdciterator 2")

        gen = self.authorized_client.get_datasets(q="pynpdciterator")

        dataset = next(gen)
        self.assertIsInstance(dataset, Dataset)
        dataset = next(gen)
        self.assertIsInstance(dataset, Dataset)

    def test_getting_datasets_with_invalid_chunk_size_fails(self) -> None:
        with pytest.raises(ValueError):
            self.anonymous_client.get_datasets(chunk_size=0)

        with pytest.raises(ValueError):
            self.anonymous_client.get_datasets(chunk_size=1000)

    # READ DATASET

    def test_read_single_public_dataset(self) -> None:
        dataset = self.anonymous_client.get_dataset(self.PUBLIC_ID)
        self.assertIsInstance(dataset, Dataset)
        if type(dataset) is not Dataset:  # make mypy happy
            raise Exception()

        self.assertEqual(dataset.id, self.PUBLIC_ID)
        self.assertEqual(dataset.type, DatasetType.PUBLIC)
        self.assertIsInstance(dataset.published, datetime)
        self.assertIsInstance(dataset.published_by, uuid.UUID)

        self.assertIsInstance(dataset.permissions, Permission)
        if type(dataset.permissions) is not Permission:  # make mypy happy
            raise Exception()
        self.assertIsInstance(dataset.permissions.may_read, bool)
        self.assertTrue(dataset.permissions.may_read)

    def test_reading_draft_dataset_without_auth_fails(self) -> None:
        dataset = self.anonymous_client.get_dataset(self.DRAFT_ID)

        self.assertIsNone(dataset)

    def test_reading_draft_dataset_with_auth(self) -> None:
        dataset = self.authorized_client.get_dataset(self.DRAFT_ID)

        self.assertIsInstance(dataset, Dataset)
        if type(dataset) is not Dataset:  # make mypy happy
            raise Exception()

        self.assertEqual(dataset.id, self.DRAFT_ID)
        self.assertEqual(dataset.type, DatasetType.DRAFT)
        self.assertIsNone(dataset.published)
        self.assertIsNone(dataset.published_by)

    def test_reading_non_existent_dataset_fails(self) -> None:
        dataset_id = uuid.uuid4()

        dataset = self.anonymous_client.get_dataset(dataset_id)

        self.assertIsNone(dataset)

    def test_reading_dataset_with_invalid_token_fails(self) -> None:
        dataset_id = uuid.uuid4()

        with pytest.raises(APIException):
            self.invalid_token_client.get_dataset(dataset_id)

    # CREATE DATASET

    def test_create_dataset(self) -> None:
        content = dict(
            title="Draft dataset created by pynpdc unit test", summary=self.tag
        )

        dataset: Optional[Dataset]

        dataset = self.authorized_client.create_dataset(content)
        self.assertIsInstance(dataset, Dataset)
        if type(dataset) is not Dataset:  # make mypy happy
            raise Exception()

        self.assertDictEqual(dataset.content, content)
        self.assertTrue(str(dataset.doi).startswith("10.21334/"))
        self.assertIsInstance(dataset.created, datetime)
        self.assertIsInstance(dataset.modified, datetime)
        self.assertEqual(dataset.created_by, self.authorized_user_id)
        self.assertEqual(dataset.modified_by, self.authorized_user_id)
        self.assertIsNone(dataset.published)
        self.assertIsNone(dataset.published_by)

        dataset = self.authorized_client.get_dataset(dataset.id)
        self.assertIsInstance(dataset, Dataset)
        if type(dataset) is not Dataset:  # make mypy happy
            raise Exception()

        self.assertDictEqual(dataset.content, content)

    def test_creating_dataset_without_auth_fails(self) -> None:
        content = dict(title="Dataset created by pynpdc unit test")

        with pytest.raises(MissingAccountException):
            self.anonymous_client.create_dataset(content)

    def test_creating_dataset_with_wrong_class_fails(self) -> None:
        content = "a string"

        with pytest.raises(ValueError):
            self.authorized_client.create_dataset(content)  # type:ignore

    # UPDATE DATASET

    def test_update_dataset(self) -> None:
        content = dict(
            title="Draft dataset for updating created by pynpdc unit test",
            summary=self.tag,
        )

        dataset: Optional[Dataset]

        dataset = self.authorized_client.create_dataset(content)
        self.assertIsInstance(dataset, Dataset)

        new_content = dict(
            title="Updated draft dataset created by pynpdc unit test", summary=self.tag
        )

        self.authorized_client.update_dataset(dataset.id, new_content)

        dataset = self.authorized_client.get_dataset(dataset.id)
        self.assertIsInstance(dataset, Dataset)
        if type(dataset) is not Dataset:  # make mypy happy
            raise Exception()

        self.assertDictEqual(dataset.content, new_content)

    def test_updating_dataset_with_wrong_class_fails(self) -> None:
        content = dict(
            title="Draft dataset for updating created by pynpdc unit test",
            summary=self.tag,
        )

        dataset = self.authorized_client.create_dataset(content)
        self.assertIsInstance(dataset, Dataset)

        with pytest.raises(ValueError):
            self.authorized_client.update_dataset(dataset.id, "a string")  # type:ignore

    # DELETE DATASET

    def test_delete_dataset(self) -> None:
        content = dict(
            title="Dataset for deletion created by pynpdc unit test", summary=self.tag
        )

        dataset: Optional[Dataset]

        dataset = self.authorized_client.create_dataset(content)
        id = dataset.id

        dataset = self.authorized_client.get_dataset(id)
        self.assertIsInstance(dataset, Dataset)
        if type(dataset) is not Dataset:  # make mypy happy
            raise Exception()

        self.assertEqual(dataset.id, id)

        self.authorized_client.delete_dataset(id)

        dataset = self.authorized_client.get_dataset(id)
        self.assertIsNone(dataset)

    def test_deleting_public_dataset_fails(self) -> None:
        with pytest.raises(APIException) as e_info:
            self.authorized_client.delete_dataset(self.PUBLIC_ID)
        self.assertEqual(e_info.value.status_code, 403)

    # PREFIX

    def test_get_prefixes(self) -> None:
        for prefixes in [
            self.anonymous_client.get_prefixes(self.PUBLIC_ID),
            self.anonymous_client.get_prefixes(self.PUBLIC_ID, recursive=True),
        ]:
            self.assertIsInstance(prefixes, PrefixCollection)
            prefix = next(prefixes)
            self.assertIsInstance(prefix, Prefix)
            self.assertEqual(prefix.dataset_id, self.PUBLIC_ID)
            self.assertEqual(prefix.prefix, "/")  # the default prefix
            self.assertGreater(prefix.file_count, 0)
            self.assertGreater(prefix.byte_size, 0)

    def test_get_empty_prefix_response(self) -> None:
        prefix = f"/.{uuid.uuid4}/"
        prefixes = list(
            self.anonymous_client.get_prefixes(self.PUBLIC_ID, prefix=prefix)
        )
        self.assertEqual(len(prefixes), 0)

    # OTHER TESTS

    def test_exec_request_with_unknown_data_type(self) -> None:
        with pytest.raises(ValueError):
            self.authorized_client._exec_request("POST", "/whatever/", data=3)


@pytest.mark.usefixtures("run_fixtures")
class TestAttachment(FixtureMethods):
    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @property
    def _file_tests(self) -> Dict[str, bytes]:
        return {
            "upload-download-1.txt": b"File content 1",
            "upload-download-2.json": b'{"content": "File content 2"}',
            "upload-download-3.tsv": b"Name\tIndex\nFile content 3\t3",
        }

    # READ ATTACHMENT COLLECTION

    def test_read_attachments_through_client(self) -> None:
        gen = self.anonymous_client.get_attachments(self.PUBLIC_ID, take=1)
        self.assertIsInstance(gen, AttachmentCollection)

        attachments = list(gen)
        self.assertEqual(len(attachments), 1)
        self.assertIsInstance(attachments[0], Attachment)
        self.assertIsInstance(attachments[0].permissions, Permission)
        self.assertEqual(attachments[0].prefix, "/")

    def test_read_attachments_through_dataset(self) -> None:
        dataset = self.anonymous_client.get_dataset(self.PUBLIC_ID)
        self.assertIsInstance(dataset, Dataset)
        if type(dataset) is not Dataset:  # make mypy happy
            raise Exception()

        gen = dataset.get_attachments(take=1)
        self.assertIsInstance(gen, AttachmentCollection)
        self.assertIsNone(gen.count)

        attachments = list(gen)
        self.assertEqual(len(attachments), 1)
        self.assertIsInstance(attachments[0], Attachment)

    def test_read_attachments_with_count(self) -> None:
        gen = self.authorized_client.get_attachments(self.PUBLIC_ID, take=1, count=True)
        attachments = list(gen)

        self.assertEqual(len(attachments), 1)
        self.assertIsInstance(gen.count, int)
        if type(gen.count) is not int:  # make mypy happy
            raise Exception()

        self.assertGreaterEqual(gen.count, 1)

    # READ ATTACHMENT METADATA

    def test_read_single_attachment(self) -> None:
        gen = self.anonymous_client.get_attachments(self.PUBLIC_ID, take=1)
        attachments = list(gen)
        self.assertEqual(len(attachments), 1)
        attachment_id = attachments[0].id

        attachment = self.anonymous_client.get_attachment(self.PUBLIC_ID, attachment_id)

        self.assertIsInstance(attachment, Attachment)
        if type(attachment) is not Attachment:  # make mypy happy
            raise Exception()

        self.assertEqual(attachment_id, attachment.id)
        self.assertEqual(attachment.prefix, "/")
        self.assertIsInstance(attachment.permissions, Permission)

    def test_reading_non_existent_attachment_fails(self) -> None:
        attachment_id = uuid.uuid4()

        attachment = self.anonymous_client.get_attachment(self.PUBLIC_ID, attachment_id)

        self.assertIsNone(attachment)

    def test_reading_attachment_with_invalid_token_fails(self) -> None:
        dataset_id = uuid.uuid4()
        attachment_id = uuid.uuid4()

        with pytest.raises(APIException):
            self.invalid_token_client.get_attachment(dataset_id, attachment_id)

    # READ ATTACHMENT CONTENT

    def test_read_attachment_content(self) -> None:
        gen = self.anonymous_client.get_attachments(self.PUBLIC_ID)
        for attachment in gen:
            if attachment.released is not None and attachment.released > datetime.now():
                continue  # embargoed (we may read meta data, but not content)

        m = hashlib.sha256()
        with attachment.reader() as src:
            for chunk in src:
                m.update(chunk)

        sha = m.hexdigest()
        self.assertEqual(attachment.sha256, sha)

    def test_write_attachment_content_to_file(self) -> None:
        """This test is more thought as a use case for documentation than a
        necessary unit test"""

        gen = self.anonymous_client.get_attachments(self.PUBLIC_ID)
        for attachment in gen:
            if attachment.released is not None and attachment.released > datetime.now():
                continue  # embargoed (we may read meta data, but not content)

        # part 1: stream content to bytes

        b = io.BytesIO()
        with attachment.reader() as src:
            for chunk in src:
                b.write(chunk)
        local_content = b.getvalue()

        # part 2: write to temp file

        with tempfile.TemporaryFile() as dest:
            with attachment.reader() as src:
                shutil.copyfileobj(src, dest)

            dest.seek(0)
            file_content = dest.read()

        self.assertEqual(local_content, file_content)

    # ADD ATTACHMENT

    def test_create_file_upload(self) -> None:
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        tests = [
            (["pynpdc", "exception.py"], "exception.py", "text/x-python"),
            (["Makefile"], "Makefile", "application/octet-stream"),
        ]

        for pp, filename, mime_type in tests:
            path = os.path.join(base_path, *pp)

            dto = self.anonymous_client.create_file_upload(path)
            self.assertIsInstance(dto, AttachmentCreateDTO)
            self.assertEqual(dto.filename, filename)
            self.assertEqual(dto.mime_type, mime_type)
            # check reader
            with open(path, "rb") as f:
                content = f.read()
            with dto.reader as f:
                self.assertEqual(content, f.read())

    def test_creating_file_upload_with_no_nexisting_file_fails(self) -> None:
        path = "this-file-does-not-exist.x"

        with pytest.raises(FileNotFoundError):
            self.anonymous_client.create_file_upload(path)

    def test_add_attachments(self) -> None:
        dataset_id = self._create_draft()

        dtos = [
            AttachmentCreateDTO(
                io.BytesIO(b"Content 1"), "test.txt", mime_type="text/plain"
            ),
            AttachmentCreateDTO(
                io.BytesIO(b"Content 2"), "test.test", mime_type="text/x-test"
            ),
        ]

        info = self.authorized_client.add_attachments(dataset_id, dtos)

        self.assertEqual(info[0].filename, "test.txt")
        self.assertEqual(info[1].filename, "test.test")
        self.assertIsInstance(info[0].sha256, str)
        self.assertIsInstance(info[1].sha256, str)

        # load 1st attachment metadata
        attachment = self.authorized_client.get_attachment(dataset_id, info[0].id)
        self.assertIsInstance(attachment, Attachment)
        if type(attachment) is not Attachment:  # make mypy happy
            raise Exception()

        self.assertEqual(attachment.filename, "test.txt")
        self.assertEqual(attachment.mime_type, "text/plain")

        # load 2nd attachment metadata
        attachment = self.authorized_client.get_attachment(dataset_id, info[1].id)
        self.assertIsInstance(attachment, Attachment)
        if type(attachment) is not Attachment:  # make mypy happy
            raise Exception()

        self.assertEqual(attachment.filename, "test.test")
        self.assertEqual(attachment.mime_type, "text/x-test")

        tests = [
            (info[0].id, b"Content 1"),
            (info[1].id, b"Content 2"),
        ]
        for attachment_id, content in tests:
            reader = self.authorized_client.get_attachment_reader(
                dataset_id, attachment_id
            )
            with reader as f:
                self.assertEqual(content, f.read())

    def test_adding_attachments_without_auth_fails(self) -> None:
        dataset_id = self._create_draft()

        dtos = [
            AttachmentCreateDTO(
                io.BytesIO(b"Content 1"), "test.txt", mime_type="text/plain"
            ),
            AttachmentCreateDTO(
                io.BytesIO(b"Content 2"), "test.test", mime_type="text/x-test"
            ),
        ]

        with pytest.raises(APIException):
            self.invalid_token_client.add_attachments(dataset_id, dtos)

    def test_add_attachment(self) -> None:
        dataset_id = self._create_draft()

        content = b"Content 3"
        dto = AttachmentCreateDTO(
            io.BytesIO(content), "test.txt", mime_type="text/plain"
        )
        dto.title = "Custom title"
        dto.description = "Custom description"

        info = self.authorized_client.add_attachment(dataset_id, dto)

        self.assertEqual(info.filename, "test.txt")

        attachment = self.authorized_client.get_attachment(dataset_id, info.id)
        self.assertIsInstance(attachment, Attachment)
        if type(attachment) is not Attachment:  # make mypy happy
            raise Exception()

        self.assertEqual(attachment.filename, "test.txt")
        self.assertEqual(attachment.mime_type, "text/plain")
        self.assertEqual(attachment.byte_size, len(content))
        self.assertEqual(attachment.title, "Custom title")
        self.assertEqual(attachment.description, "Custom description")
        self.assertIsInstance(attachment.released, datetime)

        reader = self.authorized_client.get_attachment_reader(dataset_id, info.id)
        with reader as f:
            self.assertEqual(content, f.read())

    def test_adding_attachment_without_auth_fails(self) -> None:
        dataset_id = self._create_draft()

        dto = AttachmentCreateDTO(
            io.BytesIO(b"Content 1"), "test.txt", mime_type="text/plain"
        )

        with pytest.raises(MissingAccountException):
            self.anonymous_client.add_attachment(dataset_id, dto)

    # DELETE ATTACHMENT

    def test_delete_attachment(self) -> None:
        dataset_id = self._create_draft()
        attachment_id = self._create_attachment(dataset_id, b"Content 3")

        # delete attachment
        self.authorized_client.delete_attachment(dataset_id, attachment_id)

        # try to load attachment
        attachment = self.authorized_client.get_attachment(dataset_id, attachment_id)
        self.assertEqual(attachment, None)

    # UPDATE ATTACHMENT METADATA

    def test_update_attachment(self) -> None:
        dataset_id = self._create_draft()
        attachment_id = self._create_attachment(dataset_id, b"Content 3")

        # update and check

        updated_meta = {
            "description": "Custom description",
            "filename": "custom-filename.txt",
            "prefix": "/test/",
            "title": "Custom title",
        }

        attachment: Optional[Attachment]

        attachment = self.authorized_client.update_attachment(
            dataset_id, attachment_id, **updated_meta
        )
        self.assertIsInstance(attachment, Attachment)
        if type(attachment) is not Attachment:  # make mypy happy
            raise Exception()

        self.assertEqual(attachment.description, updated_meta["description"])
        self.assertEqual(attachment.filename, updated_meta["filename"])
        self.assertEqual(attachment.title, updated_meta["title"])
        self.assertEqual(attachment.prefix, updated_meta["prefix"])

        # load attachment again and check

        attachment = self.authorized_client.get_attachment(dataset_id, attachment_id)
        self.assertIsInstance(attachment, Attachment)
        if type(attachment) is not Attachment:  # make mypy happy
            raise Exception()

        self.assertEqual(attachment.description, updated_meta["description"])
        self.assertEqual(attachment.filename, updated_meta["filename"])
        self.assertEqual(attachment.title, updated_meta["title"])

    # UPLOAD AND DOWNLOAD ATTACHMENTS AS FILES

    def test_upload_single_attachment(self) -> None:
        dataset_id = self._create_draft()

        filename = "upload-download.txt"

        with tempfile.TemporaryDirectory() as dir:
            path = os.path.join(dir, filename)

            # create local file
            content = b"File content"
            with open(path, "wb") as f:
                f.write(content)

            # upload file
            info = self.authorized_client.upload_attachment(dataset_id, path)

        self.assertIsInstance(info, AttachmentCreationInfo)
        self.assertEqual(info.filename, filename)

    def test_download_single_attachment(self) -> None:
        filename = "upload-download.txt"
        content = b"File content"
        dataset_id = self._create_draft()
        attachment_id = self._create_attachment(dataset_id, content, filename)

        # download file

        with tempfile.TemporaryDirectory() as dir:
            path = self.authorized_client.download_attachment(
                dataset_id, attachment_id, dir
            )

            self.assertIsInstance(path, str)
            if type(path) is not str:  # make mypy happy
                raise Exception()

            with open(path, "rb") as f:
                self.assertEqual(content, f.read())

    def test_upload_multiple_attachments(self) -> None:
        dataset_id = self._create_draft()
        files = self._file_tests

        with tempfile.TemporaryDirectory() as dir:
            # create local files
            paths = []
            for filename, content in files.items():
                path = os.path.join(dir, filename)
                paths.append(path)
                with open(path, "wb") as f:
                    f.write(content)

            # upload files
            info = self.authorized_client.upload_attachments(dataset_id, paths)

        want_filenames = list(files.keys())
        got_filenames = [i.filename for i in info]
        self.assertListEqual(want_filenames, got_filenames)

    def test_download_attachments_as_zip(self) -> None:
        dataset_id = self._create_draft()
        files = self._file_tests
        for filename, content in files.items():
            self._create_attachment(dataset_id, content, filename)

        with tempfile.TemporaryDirectory() as dir:
            path = self.authorized_client.download_attachments_as_zip(dataset_id, dir)

            self.assertEqual(path, f"{dir}/{dataset_id}_files.zip")
            self.assertTrue(zipfile.is_zipfile(path))

            zip_info = zipfile.ZipFile(path).infolist()
            # check the file names
            expected_filenames = files.keys()
            zip_filenames = [info.filename for info in zip_info]
            self.assertEqual(set(expected_filenames), set(zip_filenames))
            # check the content lengths
            expected_lengths = [len(content) for content in files.values()]
            zip_lengths = [info.file_size for info in zip_info]
            self.assertEqual(set(expected_lengths), set(zip_lengths))

    def test_download_attachments_as_zip_through_dataset_instance(self) -> None:
        dataset_id = self._create_draft()
        files = self._file_tests
        for filename, content in files.items():
            self._create_attachment(dataset_id, content, filename)

        dataset = self.authorized_client.get_dataset(dataset_id)
        self.assertIsInstance(dataset, Dataset)
        if type(dataset) is not Dataset:  # make mypy happy
            raise Exception()

        with tempfile.TemporaryDirectory() as dir:
            path = dataset.download_attachments_as_zip(dir)

            self.assertEqual(path, f"{dir}/{dataset_id}_files.zip")
            self.assertTrue(zipfile.is_zipfile(path))

    def test_downloading_attachments_as_zip_to_nonexisting_dir_fails(self) -> None:
        with pytest.raises(FileNotFoundError):
            self.authorized_client.download_attachments_as_zip(
                uuid.uuid4(), "this-dir-does-not-exist.x"
            )

    def test_uploading_nonexisting_file_fails(self) -> None:
        with pytest.raises(FileNotFoundError):
            self.authorized_client.upload_attachment(
                uuid.uuid4(), "this-file-does-not-exist.x"
            )

    def test_uploading_nonexisting_files_fails(self) -> None:
        with pytest.raises(FileNotFoundError):
            self.authorized_client.upload_attachments(
                uuid.uuid4(), ["this-file-does-not-exist.x"]
            )

    def test_downloading_file_to_nonexisting_dir_fails(self) -> None:
        with pytest.raises(FileNotFoundError):
            self.authorized_client.download_attachment(
                uuid.uuid4(), uuid.uuid4(), "this-dir-does-not-exist.x"
            )

    def test_downloading_from_nonexisting_attachment_fails(self) -> None:
        path = self.authorized_client.download_attachment(
            self.PUBLIC_ID, uuid.uuid4(), "/tmp"
        )
        self.assertIsNone(path)


@pytest.mark.usefixtures("run_fixtures")
class TestRecord(FixtureMethods):
    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # READ RECORD COLLECTION

    def test_read_records_through_client(self) -> None:
        # seed

        self._delete_records(self.PUBLIC_ID)
        for _ in range(2):
            self._create_record(self.PUBLIC_ID)

        # test

        gen = self.anonymous_client.get_records(self.PUBLIC_ID)
        self.assertIsInstance(gen, RecordCollection)
        self.assertIsNone(gen.count)

        records = list(gen)
        self.assertEqual(len(records), 2)
        self.assertIsInstance(records[0], Record)

    def test_read_records_through_dataset(self) -> None:
        # seed

        self._delete_records(self.PUBLIC_ID)
        for _ in range(2):
            self._create_record(self.PUBLIC_ID)

        # test

        dataset = self.anonymous_client.get_dataset(self.PUBLIC_ID)
        self.assertIsInstance(dataset, Dataset)
        if type(dataset) is not Dataset:  # make mypy happy
            raise Exception()

        gen = dataset.get_records()
        self.assertIsInstance(gen, RecordCollection)

        records = list(gen)
        self.assertEqual(len(records), 2)
        self.assertIsInstance(records[0], Record)

    def test_read_records_with_count(self) -> None:
        # seed

        self._delete_records(self.PUBLIC_ID)
        for _ in range(2):
            self._create_record(self.PUBLIC_ID)

        # test

        gen = self.authorized_client.get_records(self.PUBLIC_ID, take=1, count=True)
        attachments = list(gen)

        self.assertEqual(len(attachments), 1)
        self.assertEqual(gen.count, 2)

    # READ SINGLE RECORD

    def test_read_record_by_ids(self) -> None:
        # seed

        self._delete_records(self.PUBLIC_ID)
        record_id = self._create_record(self.PUBLIC_ID)

        # test

        record = self.anonymous_client.get_record(self.PUBLIC_ID, record_id)
        self.assertIsInstance(record, Record)

    def test_reading_non_existent_record_fails(self) -> None:
        record_id = uuid.uuid4()

        record = self.anonymous_client.get_record(self.PUBLIC_ID, record_id)

        self.assertIsNone(record)

    def test_reading_record_with_invalid_token_fails(self) -> None:
        record_id = uuid.uuid4()

        with pytest.raises(APIException):
            self.invalid_token_client.get_record(self.PUBLIC_ID, record_id)

    # ADD RECORD

    def test_add_record(self) -> None:
        now = datetime.now().isoformat()
        content = {
            "id": "test01@" + now,
            "measured": now,
            "values": [{"key": "weather", "value": "sunny"}],
        }
        dto = RecordCreateDTO(content=content, type="measurement")

        info = self.authorized_client.add_record(self.PUBLIC_ID, dto)

        self.assertIsInstance(info, RecordCreationInfo)
        self.assertEqual(info.num_processed, 1)
        self.assertEqual(info.num_created, 1)
        self.assertEqual(info.num_conflict, 0)

    def test_add_parent_child_record(self) -> None:
        now = datetime.now().isoformat()

        content = {
            "id": "test01@" + now,
            "measured": now,
            "values": [{"key": "weather", "value": "sunny"}],
        }

        parent_id = uuid.uuid4()

        parent_dto = RecordCreateDTO(content=content, type="measurement", id=parent_id)
        self.authorized_client.add_record(self.PUBLIC_ID, parent_dto)

        content["values"] = [{"key": "parentID", "value": str(parent_id)}]
        child_dto = RecordCreateDTO(
            content=content, type="measurement", parent_id=parent_id
        )
        child_info = self.authorized_client.add_record(self.PUBLIC_ID, child_dto)

        self.assertIsInstance(child_info, RecordCreationInfo)
        self.assertEqual(child_info.num_processed, 1)
        self.assertEqual(child_info.num_created, 1)
        self.assertEqual(child_info.num_conflict, 0)

        # ⚠️ at time (2024-10-28) the API lacks the possibility to retreive
        #   information about how to access the created records. Therefore
        #   we cannot test the integrity of the created data

    # DELETE RECORD

    def test_delete_record(self) -> None:
        # seed

        self._delete_records(self.PUBLIC_ID)
        record_id = self._create_record(self.PUBLIC_ID)

        # test
        self.authorized_client.delete_record(self.PUBLIC_ID, record_id)

        # try to load record
        record = self.authorized_client.get_record(self.PUBLIC_ID, record_id)
        self.assertEqual(record, None)


@pytest.mark.usefixtures("run_fixtures")
class TestPermission(unittest.TestCase, FixtureProperties):
    def setUp(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def test_create_permission(self) -> None:
        # cleanup
        try:
            self.authorized_client.delete_permission(self.DRAFT_ID, self.OTHER_USER_ID)
        except APIException:
            pass

        # add permission
        permission = self.authorized_client.add_permission(
            self.DRAFT_ID, self.OTHER_USER_ID, may_read=True, may_update=True
        )

        self.assertIsInstance(permission, Permission)
        self.assertTrue(permission.may_read)
        self.assertTrue(permission.may_update)
        self.assertFalse(permission.may_delete)
        self.assertEqual(permission.object_id, self.DRAFT_ID)
        self.assertEqual(permission.user_id, self.OTHER_USER_ID)

    def test_get_permissions(self) -> None:
        permissions = self.authorized_client.get_permissions(self.DRAFT_ID)

        self.assertIsInstance(permissions, PermissionCollection)

        executed = False
        for permission in permissions:
            self.assertIsInstance(permission, Permission)
            self.assertIsInstance(permission.user_id, uuid.UUID)
            self.assertIsInstance(permission.may_read, bool)
            self.assertIsInstance(permission.may_update, bool)
            self.assertIsInstance(permission.may_delete, bool)
            executed = True

        self.assertTrue(executed)

    def test_get_permission(self) -> None:
        permission = self.authorized_client.get_permission(
            self.DRAFT_ID, self.authorized_user_id
        )

        self.assertIsInstance(permission, Permission)
        if type(permission) is not Permission:  # make mypy happy
            raise Exception()

        self.assertEqual(permission.user_id, self.authorized_user_id)

    def test_getting_permission_with_invalid_object_id_fails(self) -> None:
        permission = self.authorized_client.get_permission(self.DRAFT_ID, uuid.uuid4())

        self.assertIsNone(permission)

    def test_getting_permission_with_unauthorized_client_fails(self) -> None:
        with pytest.raises(APIException):
            self.invalid_token_client.get_permission(
                self.DRAFT_ID, self.authorized_user_id
            )

    def test_update_permission(self) -> None:
        # cleanup
        try:
            self.authorized_client.delete_permission(self.DRAFT_ID, self.OTHER_USER_ID)
        except APIException:
            pass

        # create permission
        self.authorized_client.add_permission(self.DRAFT_ID, self.OTHER_USER_ID)

        # update permission
        permission = self.authorized_client.update_permission(
            self.DRAFT_ID, self.OTHER_USER_ID, may_read=True
        )

        self.assertIsInstance(permission, Permission)
        self.assertTrue(permission.may_read)
        self.assertFalse(permission.may_update)
        self.assertFalse(permission.may_delete)
        self.assertEqual(permission.object_id, self.DRAFT_ID)
        self.assertEqual(permission.user_id, self.OTHER_USER_ID)

    def test_delete_permission(self) -> None:
        # cleanup
        try:
            self.authorized_client.delete_permission(self.DRAFT_ID, self.OTHER_USER_ID)
        except APIException:
            pass

        # create permission
        self.authorized_client.add_permission(self.DRAFT_ID, self.OTHER_USER_ID)

        # delete permission
        self.authorized_client.delete_permission(self.DRAFT_ID, self.OTHER_USER_ID)

        # try to read this permission
        result = self.authorized_client.get_permission(
            self.DRAFT_ID, self.OTHER_USER_ID
        )
        self.assertIsNone(result)


class TestMissingClientException(unittest.TestCase):
    # in these tests Dataset and Attachment objects are created manually. This
    # should never be done manually in production code.

    def test_fail_to_call_attachment_methods_that_need_a_client(self) -> None:
        raw = AttachmentAPIResponse(
            byteSize=0,
            created=datetime.now().isoformat(),
            createdBy=str(uuid.uuid4()),
            datasetId=str(uuid.uuid4()),
            description="",
            filename="",
            id=str(uuid.uuid4()),
            mimeType="",
            modified=datetime.now().isoformat(),
            modifiedBy=str(uuid.uuid4()),
            prefix="",
            released=datetime.now().isoformat(),
            sha256="",
            title="",
            permissions=PermissionAPIResponse(
                objectId=str(uuid.uuid4()),
                userId=str(uuid.uuid4()),
                mayDelete=False,
                mayRead=False,
                mayUpdate=False,
            ),
        )

        attachment = Attachment(raw)

        with pytest.raises(MissingClientException):
            attachment.reader()

    def test_fail_to_call_dataset_methods_that_need_a_client(self) -> None:
        raw = DatasetAPIResponse(
            content={},
            created=datetime.now().isoformat(),
            createdBy=str(uuid.uuid4()),
            doi="",
            id=str(uuid.uuid4()),
            modified=datetime.now().isoformat(),
            modifiedBy=str(uuid.uuid4()),
            published=datetime.now().isoformat(),
            publishedBy="",
            type=DatasetType.DRAFT.value,
            permissions=PermissionAPIResponse(
                objectId=str(uuid.uuid4()),
                userId=str(uuid.uuid4()),
                mayDelete=False,
                mayRead=False,
                mayUpdate=False,
            ),
        )

        dataset = Dataset(raw)

        with pytest.raises(MissingClientException):
            dataset.get_attachments()

        with pytest.raises(MissingClientException):
            dataset.get_records()

        with pytest.raises(MissingClientException):
            dataset.download_attachments_as_zip("")
