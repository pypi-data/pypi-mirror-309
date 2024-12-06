class Container:
    def __init__(self, data) -> None:
        self.id = data.id
        self.short_id = data.short_id
        self.name = data.name
        self.dockercontainer = data
        self.labels = None
        if "Config" in self.dockercontainer.attrs:
            cfg = self.dockercontainer.attrs["Config"]
            if "Labels" in cfg:
                self.labels = cfg["Labels"]
        self.type = self._type()

    def _type(self):
        for label, value in self.labels.items():
            if label.startswith("com.docker.compose"):
                return "COMPOSE"
            elif label.startswith("com.docker.stack"):
                return "STACK"
        return "DOCKER"

    @staticmethod
    def formatline(
        containername, containerid, containertype
        ):
        return (
            f"{containername:32s} "
            f"{containerid:12s} "
            f"{containertype:14s}"
        )

    @staticmethod
    def underline():
        text = "="*32 + " " + "="*12 + " " + "="*14
        #     "=","=","="*13
        # )
        # newtext = text.replace("  ","++").replace("+=", " =").replace("+", "=")
        return text

    @staticmethod
    def titleText():
        return Container.formatline(
            "CONTAINER NAME", "CONTAINER ID", "CONTAINER TYPE"
        )

    def __repr__(self) -> str:
        return Container.formatline(self.name, self.short_id, self.type)
