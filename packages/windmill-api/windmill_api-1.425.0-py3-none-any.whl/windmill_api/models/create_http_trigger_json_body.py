from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_http_trigger_json_body_http_method import CreateHttpTriggerJsonBodyHttpMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_http_trigger_json_body_static_asset_config import CreateHttpTriggerJsonBodyStaticAssetConfig


T = TypeVar("T", bound="CreateHttpTriggerJsonBody")


@_attrs_define
class CreateHttpTriggerJsonBody:
    """
    Attributes:
        path (str):
        script_path (str):
        route_path (str):
        is_flow (bool):
        http_method (CreateHttpTriggerJsonBodyHttpMethod):
        is_async (bool):
        requires_auth (bool):
        static_asset_config (Union[Unset, CreateHttpTriggerJsonBodyStaticAssetConfig]):
    """

    path: str
    script_path: str
    route_path: str
    is_flow: bool
    http_method: CreateHttpTriggerJsonBodyHttpMethod
    is_async: bool
    requires_auth: bool
    static_asset_config: Union[Unset, "CreateHttpTriggerJsonBodyStaticAssetConfig"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        script_path = self.script_path
        route_path = self.route_path
        is_flow = self.is_flow
        http_method = self.http_method.value

        is_async = self.is_async
        requires_auth = self.requires_auth
        static_asset_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.static_asset_config, Unset):
            static_asset_config = self.static_asset_config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "script_path": script_path,
                "route_path": route_path,
                "is_flow": is_flow,
                "http_method": http_method,
                "is_async": is_async,
                "requires_auth": requires_auth,
            }
        )
        if static_asset_config is not UNSET:
            field_dict["static_asset_config"] = static_asset_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_http_trigger_json_body_static_asset_config import (
            CreateHttpTriggerJsonBodyStaticAssetConfig,
        )

        d = src_dict.copy()
        path = d.pop("path")

        script_path = d.pop("script_path")

        route_path = d.pop("route_path")

        is_flow = d.pop("is_flow")

        http_method = CreateHttpTriggerJsonBodyHttpMethod(d.pop("http_method"))

        is_async = d.pop("is_async")

        requires_auth = d.pop("requires_auth")

        _static_asset_config = d.pop("static_asset_config", UNSET)
        static_asset_config: Union[Unset, CreateHttpTriggerJsonBodyStaticAssetConfig]
        if isinstance(_static_asset_config, Unset):
            static_asset_config = UNSET
        else:
            static_asset_config = CreateHttpTriggerJsonBodyStaticAssetConfig.from_dict(_static_asset_config)

        create_http_trigger_json_body = cls(
            path=path,
            script_path=script_path,
            route_path=route_path,
            is_flow=is_flow,
            http_method=http_method,
            is_async=is_async,
            requires_auth=requires_auth,
            static_asset_config=static_asset_config,
        )

        create_http_trigger_json_body.additional_properties = d
        return create_http_trigger_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
