from fastapi import APIRouter

from src.main.rest.atleta_detail import atleta_detail
from src.main.rest.atleta_list import atleta
from src.main.rest.competicao_list import competicao
from src.main.rest.lesao_list import lesao
from src.main.rest.relacionamento_list import relacionamento

router = APIRouter()

router.add_api_route(
    "/atleta",
    endpoint=atleta,
    methods=["GET"],
    include_in_schema=True,
)
router.add_api_route(
    "/atleta/{id}",
    endpoint=atleta_detail,
    methods=["GET"],
    include_in_schema=True,
)
router.add_api_route(
    "/questionario/relacionamento/atleta/{id}",
    endpoint=relacionamento,
    methods=["GET"],
    include_in_schema=True,
)
router.add_api_route(
    "/competicao/atleta/{id}",
    endpoint=competicao,
    methods=["GET"],
    include_in_schema=True,
)
router.add_api_route(
    "/lesao/atleta/{id}",
    endpoint=lesao,
    methods=["GET"],
    include_in_schema=True,
)
# router.add_api_route(
#     "/regras-ia-recomendacao",
#     endpoint=recomendacao_list,
#     methods=["POST"],
#     responses={
#         400: {"model": BadRequestError},
#         401: {"model": UnauthorizedError},
#         404: {"model": NotFoundError},
#         422: {"model": UnprocessableEntityError},
#         500: {"model": InternalServerError},
#     },
#     name="Recomendação de produtos baseado em regras de IA.",
#     openapi_extra={
#         "requestBody": {
#             "content": {
#                 "application/json": {
#                     "schema": {
#                         "required": ["algoritmo", "produtos_sku"],
#                         "type": "object",
#                         "properties": {
#                             "algoritmo": {"type": "string"},
#                             "produtos_sku": {
#                                 "type": "array",
#                                 "items": {"type": "string"},
#                             },
#                         },
#                     }
#                 }
#             },
#             "required": True,
#         },
#     },
#     tags=["Recomendação de produtos"],
# )


def init_app(app):
    app.include_router(router)
