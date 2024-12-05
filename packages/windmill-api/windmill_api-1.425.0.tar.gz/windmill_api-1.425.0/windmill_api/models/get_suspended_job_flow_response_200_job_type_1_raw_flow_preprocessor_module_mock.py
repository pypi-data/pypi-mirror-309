from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSuspendedJobFlowResponse200JobType1RawFlowPreprocessorModuleMock")


@_attrs_define
class GetSuspendedJobFlowResponse200JobType1RawFlowPreprocessorModuleMock:
    """
    Attributes:
        enabled (Union[Unset, bool]):
        return_value (Union[Unset, Any]):
    """

    enabled: Union[Unset, bool] = UNSET
    return_value: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        return_value = self.return_value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if return_value is not UNSET:
            field_dict["return_value"] = return_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        return_value = d.pop("return_value", UNSET)

        get_suspended_job_flow_response_200_job_type_1_raw_flow_preprocessor_module_mock = cls(
            enabled=enabled,
            return_value=return_value,
        )

        get_suspended_job_flow_response_200_job_type_1_raw_flow_preprocessor_module_mock.additional_properties = d
        return get_suspended_job_flow_response_200_job_type_1_raw_flow_preprocessor_module_mock

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
