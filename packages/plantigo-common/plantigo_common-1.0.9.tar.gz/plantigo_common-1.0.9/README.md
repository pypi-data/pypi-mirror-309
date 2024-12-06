# Plantigo Common

Welcome to the **Plantigo Common** repository. This repository contains reusable packages and shared components for the Plantigo project.

## Overview

The purpose of this repository is to centralize common code that can be shared across multiple services and applications within the Plantigo ecosystem. By doing so, we aim to reduce code duplication and improve maintainability.

## Packages

The library consists of the following packages:

* **django** - Django-specific utilities and extensions:
  * `proto_serializer.py` - Serializers for working with Protocol Buffers in Django

* **python/auth** - Authentication and authorization components:
  * `token_service.py` - Service for token management and validation

* **python/grpc** - gRPC-related utilities and infrastructure:
  * `auth_interceptor.py` - Authentication interceptor for gRPC calls
  * `rpc_caller.py` - Implementation for making gRPC service calls

The packages provide reusable components focused on Django integration, authentication handling, and gRPC communication infrastructure that can be shared across different Plantigo services.

## Contributing

We welcome contributions to the Plantigo Common repository. If you have a bug fix or a new feature to propose, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for contributing to the Plantigo project!
