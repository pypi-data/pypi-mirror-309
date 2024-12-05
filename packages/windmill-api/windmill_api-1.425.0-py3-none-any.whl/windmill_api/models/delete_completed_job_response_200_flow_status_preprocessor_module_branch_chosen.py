from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delete_completed_job_response_200_flow_status_preprocessor_module_branch_chosen_type import (
    DeleteCompletedJobResponse200FlowStatusPreprocessorModuleBranchChosenType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteCompletedJobResponse200FlowStatusPreprocessorModuleBranchChosen")


@_attrs_define
class DeleteCompletedJobResponse200FlowStatusPreprocessorModuleBranchChosen:
    """
    Attributes:
        type (DeleteCompletedJobResponse200FlowStatusPreprocessorModuleBranchChosenType):
        branch (Union[Unset, int]):
    """

    type: DeleteCompletedJobResponse200FlowStatusPreprocessorModuleBranchChosenType
    branch: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        branch = self.branch

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if branch is not UNSET:
            field_dict["branch"] = branch

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = DeleteCompletedJobResponse200FlowStatusPreprocessorModuleBranchChosenType(d.pop("type"))

        branch = d.pop("branch", UNSET)

        delete_completed_job_response_200_flow_status_preprocessor_module_branch_chosen = cls(
            type=type,
            branch=branch,
        )

        delete_completed_job_response_200_flow_status_preprocessor_module_branch_chosen.additional_properties = d
        return delete_completed_job_response_200_flow_status_preprocessor_module_branch_chosen

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
