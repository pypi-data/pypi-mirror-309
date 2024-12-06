from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from documente_shared.application.time_utils import get_datetime_from_data
from documente_shared.domain.enums import (
    DocumentProcessStatus,
    DocumentProcessSubCategory,
    DocumentProcessCategory,
)


@dataclass
class DocumentProcess(object):
    digest: str
    status: DocumentProcessStatus
    file_path: str
    file_bytes: Optional[bytes] = None
    category: Optional[DocumentProcessCategory] = None
    sub_category: Optional[DocumentProcessSubCategory] = None
    processed_csv_path: Optional[str] = None
    processed_csv_bytes: Optional[bytes] = None
    processed_xlsx_path: Optional[str] = None
    processed_xlsx_bytes: Optional[bytes] = None
    processing_time: Optional[Decimal] = None
    uploaded_at: Optional[datetime] = None
    enqueued_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def is_pending(self) -> bool:
        return self.status == DocumentProcessStatus.PENDING

    @property
    def is_enqueued(self) -> bool:
        return self.status == DocumentProcessStatus.ENQUEUED

    @property
    def is_processing(self) -> bool:
        return self.status == DocumentProcessStatus.PROCESSING

    @property
    def is_completed(self) -> bool:
        return self.status == DocumentProcessStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        return self.status == DocumentProcessStatus.FAILED

    @property
    def is_valid(self) -> bool:
        return all([
            self.digest,
            self.status,
            self.file_path,
        ])

    def enqueue(self):
        self.status = DocumentProcessStatus.ENQUEUED
        self.enqueued_at = datetime.now()

    def processing(self):
        self.status = DocumentProcessStatus.PROCESSING
        self.started_at = datetime.now()

    def failed(self):
        self.status = DocumentProcessStatus.FAILED
        self.failed_at = datetime.now()

    def completed(self):
        self.status = DocumentProcessStatus.COMPLETED
        self.completed_at = datetime.now()

    def deleted(self):
        self.status = DocumentProcessStatus.DELETED

    @property
    def extended_filename(self) -> str:
        return self.file_path.split('/')[-1]

    @property
    def filename(self) -> str:
        filename_with_extension = self.extended_filename
        return filename_with_extension.split('.')[0]

    @property
    def to_dict(self) -> dict:
        return {
            'digest': self.digest,
            'status': self.status.value,
            'file_path': self.file_path,
            'category': (
                str(self.category)
                if self.category else None
            ),
            'sub_category': (
                str(self.sub_category)
                if self.sub_category else None
            ),
            'processed_csv_path': self.processed_csv_path,
            'processed_xlsx_path': self.processed_xlsx_path,
            'processing_time': (
                str(self.processing_time)
                if self.processing_time else None
            ),
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'enqueued_at': self.enqueued_at.isoformat() if self.enqueued_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'failed_at': self.failed_at.isoformat() if self.failed_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }

    def overload(
        self,
        new_instance: 'DocumentProcess',
        properties: List[str] = None,
    ):
        instance_properties = properties or [
            'status', 'file_path', 'file_bytes', 'category', 'sub_category',
            'processed_csv_path', 'processed_csv_bytes', 'processed_xlsx_path',
            'processed_xlsx_bytes', 'processing_time', 'uploaded_at',
            'enqueued_at', 'started_at', 'failed_at', 'completed_at',
        ]
        for _property in instance_properties:
            property_value = getattr(new_instance, _property)
            if not hasattr(self, _property):
                continue
            setattr(self, _property, property_value)
        return self

    @classmethod
    def from_dict(cls, data: dict) -> 'DocumentProcess':
        return cls(
            digest=data.get('digest'),
            status=DocumentProcessStatus.from_value(data.get('status')),
            file_path=data.get('file_path'),
            category=(
                DocumentProcessCategory.from_value(data.get('category'))
                if data.get('category') else None
            ),
            sub_category=(
                DocumentProcessSubCategory.from_value(data.get('sub_category'))
                if data.get('sub_category') else None
            ),
            processed_csv_path=data.get('processed_csv_path'),
            processed_xlsx_path=data.get('processed_xlsx_path'),
            processing_time=(
                Decimal(data.get('processing_time'))
                if data.get('processing_time') else None
            ),
            uploaded_at=get_datetime_from_data(input_datetime=data.get('uploaded_at')),
            enqueued_at=get_datetime_from_data(input_datetime=data.get('enqueued_at')),
            started_at=get_datetime_from_data(input_datetime=data.get('started_at')),
            failed_at=get_datetime_from_data(input_datetime=data.get('failed_at')),
            completed_at=get_datetime_from_data(input_datetime=data.get('completed_at')),
        )