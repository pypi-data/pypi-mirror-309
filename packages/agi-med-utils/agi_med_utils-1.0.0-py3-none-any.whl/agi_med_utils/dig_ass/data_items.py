import typing as t


class ReplicaItem:
    def __init__(self, replica: dict[str, t.Any]) -> None:
        self.Body = replica["Body"]
        self.Role = replica["Role"]
        self.DateTime = replica["DateTime"]

    def to_dict(self) -> dict[str, t.Any]:
        return {
            "Body": self.Body,
            "Role": self.Role,
            "DateTime": self.DateTime,
        }


class InnerContextItem:
    def __init__(self, inner_context: dict[str, list[dict[str, t.Any]]]) -> None:
        self.Replicas = [ReplicaItem(r) for r in inner_context["Replicas"]]

    def to_dict(self) -> dict[str, list[dict[str, t.Any]]]:
        return {"Replicas": [r.to_dict() for r in self.Replicas]}


class OuterContextItem:
    def __init__(self, outer_context: dict[str, t.Any]) -> None:
        self.Sex = outer_context["Sex"]
        self.Age = outer_context["Age"]
        self.UserId = outer_context["UserId"]
        self.SessionId = outer_context["SessionId"]
        self.ClientId = outer_context["ClientId"]
        self.TrackId = outer_context.get("TrackId", "")

    def to_dict(self) -> dict[str, t.Any]:
        return {
            "Sex": self.Body,
            "Age": self.Age,
            "UserId": self.UserId,
            "SessionId": self.SessionId,
            "ClientId": self.ClientId,
            "TrackId": self.TrackId,
        }


class ChatItem:
    def __init__(self, chat: dict[str, t.Any]) -> None:
        self.OuterContext = OuterContextItem(chat["OuterContext"])
        self.InnerContext = InnerContextItem(chat["InnerContext"])

    def to_dict(self) -> dict[str, t.Any]:
        return {"OuterContext": self.OuterContext.to_dict(), "InnerContext": self.InnerContext.to_dict()}
