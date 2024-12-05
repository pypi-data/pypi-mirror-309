from typing import Any, Callable
import grpc
from plantigo_common.auth.token_service import verify_token
from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException


class AuthInterceptor(ServerInterceptor):

    def __init__(self, jwt_secret_key: str, jwt_algorithm: str):
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm

    def intercept(
        self,
        method: Callable[..., Any],
        request_or_iterator: Any,
        context: grpc.ServicerContext,
        method_name: str,
    ) -> Any:
        auth_token = dict(context.invocation_metadata()).get("authorization")

        if not auth_token or not auth_token.startswith("Bearer "):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Unauthenticated")

        token = auth_token.split(" ")[1]

        try:
            token_data = verify_token(token, self.jwt_secret_key, self.jwt_algorithm)
            user_id = token_data.get("user_id")
            context.user_id = user_id
            return method(request_or_iterator, context)
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise
