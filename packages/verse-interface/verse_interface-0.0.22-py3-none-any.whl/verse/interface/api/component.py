from verse.core import Component


class API(Component):
    component: Component
    api_keys: list[str] | None
    port: int

    def __init__(
        self,
        component: Component,
        api_keys: list[str] | None = None,
        port: int = 8000,
        **kwargs,
    ):
        """Initialize.

        Args:
            component:
                Component to host as API.
            api_keys:
                API keys for authenticated access.
            port:
                HTTP port.
        """
        self.component = component
        self.api_keys = api_keys
        self.port = port
        super().__init__(**kwargs)
