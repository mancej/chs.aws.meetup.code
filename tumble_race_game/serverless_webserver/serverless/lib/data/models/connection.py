import logging
from dataclasses import dataclass
from typing import List, Dict, Set

log = logging.getLogger(__name__)


@dataclass
class Subscription:
    event_type: str
    filter_field: str
    filter_expr: str
    desired_fields: List[str]

    @staticmethod
    def from_value(item: Dict):
        """
        Converts a boto3 item value of `subscription` into this object
        :return: Hydrated subscription object
        """

        return Subscription(
            event_type=item.get("event_type"),
            filter_field=item.get("filter_field"),
            filter_expr=item.get("filter_expr"),
            desired_fields=item.get("desired_fields")
        )

    def to_dict(self):
        return {
            "event_type": self.event_type,
            "filter_field": self.filter_field,
            "filter_expr": self.filter_expr,
            "desired_fields": self.desired_fields
        }

    def __eq__(self, obj):
        return self.event_type == obj.event_type and \
               self.filter_field == obj.filter_field and \
               self.filter_expr == obj.filter_expr

    def __hash__(self):
        return hash(f"{self.event_type}-{self.filter_field}-{self.filter_expr}")

    def __str__(self):
        return f"{self.__dict__}"


@dataclass
class Connection:
    id: str
    domain_name: str
    event_type: str
    filter_field: str
    filter_expr: str
    stage: str
    ttl: int
    subscriptions: Set[Subscription]
    is_gone: bool = False

    def add_subscription(self, sub: Subscription):
        self.subscriptions.add(sub)

    @staticmethod
    def from_item(item: Dict):
        """
        Converts a boto3 item dict into a Connection
        :param item: boto3 item from a boto3 result
        :return: hydrated connection object
        """
        log.debug(f"Getting item from item: {item}")
        if item:
            return Connection(
                id=item.get('connection_id'),
                domain_name=item.get('domain_name'),
                event_type=item.get('event_type'),
                filter_field=item.get('filter_field'),
                filter_expr=item.get('filter_expression'),
                stage=item.get('stage'),
                ttl=item.get('ttl'),
                subscriptions=set([Subscription.from_value(sub) for sub in item.get('subscriptions')])
            )
        else:
            return None

    def __str__(self):
        return f"{self.__dict__}"
