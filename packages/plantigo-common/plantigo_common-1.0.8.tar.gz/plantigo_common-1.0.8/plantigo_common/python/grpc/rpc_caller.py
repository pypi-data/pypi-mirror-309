from typing import Dict, Any, TypeVar, TypeAlias, Type
from dataclasses import dataclass
import grpc

GRPCStub = TypeVar('GRPCStub')
GRPCRequest = TypeVar('GRPCRequest')
StubType: TypeAlias = Type[GRPCStub]
RequestClassType: TypeAlias = Type[GRPCRequest]


@dataclass
class GRPCServiceConfig:
    """Configuration for a single gRPC service."""
    stub: StubType
    address: str
    request_classes: Dict[str, RequestClassType]

    def __post_init__(self):
        """Validate the configuration after initialization."""
        if not isinstance(self.address, str):
            raise ValueError("Address must be a string")
        if not self.address:
            raise ValueError("Address cannot be empty")
        if not isinstance(self.request_classes, dict):
            raise ValueError("Request classes must be a dictionary")
        if not self.request_classes:
            raise ValueError("Request classes cannot be empty")


@dataclass
class GRPCServicesConfig:
    """Configuration for all gRPC services."""
    services: Dict[str, GRPCServiceConfig]

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Dict[str, Any]]) -> 'GRPCServicesConfig':
        """
        Create GRPCServicesConfig from a dictionary.

        Args:
            config_dict: Dictionary with service configurations

        Returns:
            GRPCServicesConfig instance
        """
        services = {
            service_name: GRPCServiceConfig(
                stub=service_config["stub"],
                address=service_config["address"],
                request_classes=service_config["request_classes"]
            )
            for service_name, service_config in config_dict.items()
        }
        return cls(services=services)


class GRPCClient:
    def __init__(self, stub_class: StubType, address: str):
        """
        gRPC client for a specific stub.

        Args:
            stub_class: The gRPC stub class.
            address (str): The gRPC server address.
        """
        # TODO: Add support for secure channels on production
        self.channel = grpc.insecure_channel(address)
        self.stub = stub_class(self.channel)

    def call_method(self, method_name: str, grpc_request, metadata: list = None):
        """
        Calls a gRPC method.

        Args:
            method_name (str): The name of the method to call.
            grpc_request: The request object for the gRPC method.
            metadata (list): Metadata headers.

        Returns:
            The response from the gRPC method.
        """
        method = getattr(self.stub, method_name, None)
        if not method:
            raise ValueError(f"Method '{method_name}' not found in stub.")
        return method(grpc_request, metadata=metadata)


class GRPCServiceFacade:

    def __init__(self, request, service_name: str, services_config: GRPCServicesConfig):
        """
        Facade managing gRPC calls for a specific service.

        Args:
            request: HTTP object containing authentication data.
            service_name: Name of the service (e.g., 'devices').
            services_config: Configuration object for all gRPC services.
        """
        self.request = request
        self.metadata = [("authorization", f"Bearer {self.request.auth.token.decode('utf-8')}")]
        self.service_name = service_name

        if service_name not in services_config.services:
            raise ValueError(f"Service '{service_name}' not found in configuration.")

        service_config = services_config.services[service_name]
        self.client = GRPCClient(service_config.stub, service_config.address)
        self.request_classes = service_config.request_classes

    def call(self, method: str):
        """
        Calls a method in the gRPC service.

        Args:
            method: The name of the gRPC method.

        Returns:
            The response from the gRPC service.
        """
        if method not in self.request_classes:
            raise ValueError(f"Method '{method}' not configured for service '{self.service_name}'")

        grpc_request = self.request_classes[method]()
        return self.client.call_method(method, grpc_request, metadata=self.metadata)


class GRPCServiceFactory:
    """
    Factory creating gRPC service classes based on `GRPCServiceFacade.grpc_services`.
    """

    def __init__(self, config: GRPCServicesConfig):
        """
        Initialize factory with services configuration.

        Args:
            config: Dictionary containing configuration for all gRPC services.
        """
        self.services_config = config

    def create_service_class(self, service_name):
        """
        Creates a service class based on the name.

        Args:
            service_name: The name of the service (e.g., 'devices').

        Returns:
            A service class with methods based on gRPC methods.
        """
        facade_class = GRPCServiceFacade
        services_config = self.services_config

        class DynamicGRPCService(facade_class):
            def __init__(self, request):
                super().__init__(request, service_name, services_config)

            def __getattr__(self, name):
                method_name = "".join(part.capitalize() for part in name.split("_"))
                if method_name in self.request_classes:
                    return lambda: self.call(method_name)
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        return DynamicGRPCService


def create_grpc_services_factory(config_dict: Dict[str, Dict[str, Any]]) -> GRPCServiceFactory:
    """
    Create a GRPCServiceFactory with the provided configuration.

    Args:
        config_dict: Configuration dictionary for gRPC services.

    Returns:
        Configured GRPCServiceFactory instance.
    """
    config = GRPCServicesConfig.from_dict(config_dict)
    return GRPCServiceFactory(config)
