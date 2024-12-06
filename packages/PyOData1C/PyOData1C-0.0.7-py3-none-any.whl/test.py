from datetime import datetime
from pprint import pprint

from pydantic import Field, UUID1, field_serializer

from PyOData1C.http import Connection, auth
from PyOData1C.models import ODataModel
from PyOData1C.odata import OData


class StageModel(ODataModel):
    uid_1c: UUID1 = Field(alias='Ref_Key',
                          exclude=True)
    number: str = Field(alias='Number')
    stage_date: datetime = Field(alias='Date')

    @field_serializer('stage_date')
    def serialize_stage_date(self, stage_date: datetime, _info):
        return stage_date.isoformat('T', 'seconds')


class StageOdata(OData):
    database = 'erp_dev'
    entity_model = StageModel
    entity_name = 'Document_ЭтапПроизводства2_2'


# data = {'Number': 's2', 'Date': '2024-11-01T00:00:00'}



with Connection('erp.polipak.local',
                'http',
                auth.HTTPBasicAuth('КравцунАВ'.encode(), '2882ak')) as conn:
    manager = StageOdata.manager(conn)
    stages: list[str] = manager.top(3).all()
    pprint(manager.request)
    pprint(manager.response.json())


# class ProductModel(ODataModel):
#     uid_1c: UUID1 = Field(alias='Номенклатура_Key',
#                           exclude=True)
#     quantity: Decimal = Field(alias='Количество')


# class StageModel(ODataModel):
#     uid_1c: UUID1 = Field(alias='Ref_Key',
#                           exclude=True)
#     number: str = Field(alias='Number',
#                         min_length=1,
#                         max_length=200)
#     stage_date: datetime = Field(alias='Date')
#     status: str = Field(alias='Статус', )
#     products: list[ProductModel] = Field(alias='ВыходныеИзделия', exclude=True)
#
#     nested_models = {
#         'products': ProductModel,
#     }
#
#     @field_serializer('stage_date')
#     def serialize_stage_date(self, stage_date: datetime, _info):
#         return stage_date.isoformat('T', 'seconds')
#
#
# class StageOdata(OData):
#     database = 'erp_dev'
#     entity_model = StageModel
#     entity_name = 'Document_ЭтапПроизводства2_2'
#
#
# with Connection('erp.polipak.local',
#                 'http',
#                 auth.HTTPBasicAuth('КравцунАВ'.encode(), '2882ak')) as conn:
#     manager = StageOdata.manager(conn)
#     stage = manager.get(guid='4ab2c2af-8a36-11ec-aa39-ac1f6bd30991')
#     stage.stage_date = datetime.now()
#     stage = manager.update(stage.uid_1c, stage)
#     pprint(stage.model_dump(by_alias=True))
#     # pprint(manager.request)
#     # print(stage)
#     # pprint(manager.response)
