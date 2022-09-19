from sqlalchemy import Column, String

from service_app.data_gateway.models._base import DatedModel


class DeviceAlchemyModel(DatedModel):
    __tablename__ = "device"

    id = Column(String(length=100), primary_key=True)
    name = Column(String(length=50))
    firmware_version = Column(String(length=50))
