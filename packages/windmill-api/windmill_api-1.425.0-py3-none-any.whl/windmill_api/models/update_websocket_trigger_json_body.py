from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.update_websocket_trigger_json_body_filters_item import UpdateWebsocketTriggerJsonBodyFiltersItem
    from ..models.update_websocket_trigger_json_body_initial_messages_item_type_0 import (
        UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0,
    )
    from ..models.update_websocket_trigger_json_body_initial_messages_item_type_1 import (
        UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1,
    )
    from ..models.update_websocket_trigger_json_body_url_runnable_args import (
        UpdateWebsocketTriggerJsonBodyUrlRunnableArgs,
    )


T = TypeVar("T", bound="UpdateWebsocketTriggerJsonBody")


@_attrs_define
class UpdateWebsocketTriggerJsonBody:
    """
    Attributes:
        url (str):
        path (str):
        script_path (str):
        is_flow (bool):
        filters (List['UpdateWebsocketTriggerJsonBodyFiltersItem']):
        initial_messages (List[Union['UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0',
            'UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1']]):
        url_runnable_args (UpdateWebsocketTriggerJsonBodyUrlRunnableArgs):
    """

    url: str
    path: str
    script_path: str
    is_flow: bool
    filters: List["UpdateWebsocketTriggerJsonBodyFiltersItem"]
    initial_messages: List[
        Union[
            "UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0",
            "UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1",
        ]
    ]
    url_runnable_args: "UpdateWebsocketTriggerJsonBodyUrlRunnableArgs"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.update_websocket_trigger_json_body_initial_messages_item_type_0 import (
            UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0,
        )

        url = self.url
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        initial_messages = []
        for initial_messages_item_data in self.initial_messages:
            initial_messages_item: Dict[str, Any]

            if isinstance(initial_messages_item_data, UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0):
                initial_messages_item = initial_messages_item_data.to_dict()

            else:
                initial_messages_item = initial_messages_item_data.to_dict()

            initial_messages.append(initial_messages_item)

        url_runnable_args = self.url_runnable_args.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "filters": filters,
                "initial_messages": initial_messages,
                "url_runnable_args": url_runnable_args,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_websocket_trigger_json_body_filters_item import UpdateWebsocketTriggerJsonBodyFiltersItem
        from ..models.update_websocket_trigger_json_body_initial_messages_item_type_0 import (
            UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0,
        )
        from ..models.update_websocket_trigger_json_body_initial_messages_item_type_1 import (
            UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1,
        )
        from ..models.update_websocket_trigger_json_body_url_runnable_args import (
            UpdateWebsocketTriggerJsonBodyUrlRunnableArgs,
        )

        d = src_dict.copy()
        url = d.pop("url")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = UpdateWebsocketTriggerJsonBodyFiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        initial_messages = []
        _initial_messages = d.pop("initial_messages")
        for initial_messages_item_data in _initial_messages:

            def _parse_initial_messages_item(
                data: object,
            ) -> Union[
                "UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0",
                "UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    initial_messages_item_type_0 = UpdateWebsocketTriggerJsonBodyInitialMessagesItemType0.from_dict(
                        data
                    )

                    return initial_messages_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                initial_messages_item_type_1 = UpdateWebsocketTriggerJsonBodyInitialMessagesItemType1.from_dict(data)

                return initial_messages_item_type_1

            initial_messages_item = _parse_initial_messages_item(initial_messages_item_data)

            initial_messages.append(initial_messages_item)

        url_runnable_args = UpdateWebsocketTriggerJsonBodyUrlRunnableArgs.from_dict(d.pop("url_runnable_args"))

        update_websocket_trigger_json_body = cls(
            url=url,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            filters=filters,
            initial_messages=initial_messages,
            url_runnable_args=url_runnable_args,
        )

        update_websocket_trigger_json_body.additional_properties = d
        return update_websocket_trigger_json_body

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
