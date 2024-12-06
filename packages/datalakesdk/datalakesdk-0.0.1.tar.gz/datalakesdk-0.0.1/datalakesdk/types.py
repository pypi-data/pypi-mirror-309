from pydantic import BaseModel

class Resolution(BaseModel):
    width: int
    height: int

class FileMeta(BaseModel):
    resolution: Resolution
    tokenLength: int
    duration: int

class UploadFileResponse(BaseModel):
    url: str
    object_name: str
    uid: str
    meta: FileMeta

class UploadRawDataResponse(BaseModel):
    raw_data_id: str

class UploadAnnotationDataResponse(BaseModel):
    annotation_data_id: str

class CreateDataSetResponse(BaseModel):
    dataset_id: str

class SummaryAndDownloadDataSetResponse(BaseModel):
    url: str
    bucket: str
    object_name: str