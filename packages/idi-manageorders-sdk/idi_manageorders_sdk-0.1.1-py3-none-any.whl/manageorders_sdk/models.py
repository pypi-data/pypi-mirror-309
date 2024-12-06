"""Models."""

from typing import Literal

from pydantic import BaseModel, Field

DATE_REGEX = "[0-9]{2}/[0-9]{2}/[0-9]{4}|[0-9]{2}"


class Design(BaseModel):
    """Design."""

    design_number: int = Field(serialization_alias="id_Design")
    design_type: int = Field(serialization_alias="id_DesignType")


class LineItem(BaseModel):
    """LineItem."""

    part_number: str = Field(serialization_alias="PartNumber")
    product_class: int = Field(serialization_alias="id_ProductClass")
    quantity: int = Field(serialization_alias="Qty")

    external_shipment_id: str = Field(serialization_alias="ExtShipID")


class Address(BaseModel):
    """Address."""

    external_shipment_id: str | None = Field(None, serialization_alias="ExtShipID")

    shipping_method: str | None = Field(None, serialization_alias="ShipMethod")

    company: str | None = Field(None, serialization_alias="ShipCompany")
    address1: str | None = Field(None, serialization_alias="ShipAddress01")
    address2: str | None = Field(None, serialization_alias="ShipAddress02")
    city: str | None = Field(None, serialization_alias="ShipCity")
    state: str | None = Field(None, serialization_alias="ShipState")
    postal_code: str | None = Field(None, serialization_alias="ShipZip")
    country: str | None = Field(None, serialization_alias="ShipCountry")


class Note(BaseModel):
    """Note."""

    note: str
    type_: Literal["Notes To Production", "Notes To Shipping"] = Field(serialization_alias="Type")


class Order(BaseModel):
    """Order."""

    external_order_id: str = Field(serialization_alias="ExtOrderID")
    external_source: str = Field(serialization_alias="ExtSource")

    order_type: int = Field(serialization_alias="id_OrderType")
    employee_created_by: int = Field(serialization_alias="id_EmpCreatedBy")
    customer_id: int = Field(serialization_alias="id_Customer")
    customer_purchase_order: str = Field(serialization_alias="CustomerPurchaseOrder")
    ship_date: str = Field(pattern=DATE_REGEX, serialization_alias="date_OrderRequestedToShip")

    designs: list[Design] = Field(serialization_alias="Designs")
    line_items: list[LineItem] = Field(serialization_alias="LineItems")
    addresses: list[Address] = Field(serialization_alias="ShippingAddresses")
    notes: list[Note] = Field(serialization_alias="Notes")
