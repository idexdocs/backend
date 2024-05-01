from fastapi import APIRouter

from src.main.rest.atleta_create import atleta_create
from src.main.rest.atleta_detail import atleta_detail
from src.main.rest.atleta_list import atleta
from src.main.rest.clube_list import clube
from src.main.rest.competicao_list import competicao
from src.main.rest.lesao_list import lesao
from src.main.rest.relacionamento_create import relacionamento_create
from src.main.rest.relacionamento_list import relacionamento
from src.schemas.atleta import AtletaCreateSchema
from src.schemas.relacionamento import (
    RelacionamentoCreateSchema,
    RelacionamentoResponse,
)

router = APIRouter()

router.add_api_route(
    '/atleta',
    endpoint=atleta,
    methods=['GET'],
    include_in_schema=True,
    openapi_extra={
        'parameters': [
            {
                'in': 'query',
                'name': 'atleta',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'posicao',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'clube',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ]
    },
)
router.add_api_route(
    '/atleta/{id}',
    endpoint=atleta_detail,
    methods=['GET'],
    include_in_schema=True,
)
router.add_api_route(
    '/questionario/relacionamento/atleta/{id}',
    endpoint=relacionamento,
    methods=['GET'],
    include_in_schema=True,
)
router.add_api_route(
    '/competicao/atleta/{id}',
    endpoint=competicao,
    methods=['GET'],
    include_in_schema=True,
)
router.add_api_route(
    '/lesao/atleta/{id}',
    endpoint=lesao,
    methods=['GET'],
    include_in_schema=True,
)
router.add_api_route(
    '/create/atleta',
    endpoint=atleta_create,
    methods=['POST'],
    include_in_schema=True,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': AtletaCreateSchema.model_json_schema()
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/questionario/relacionamento/create',
    endpoint=relacionamento_create,
    methods=['POST'],
    response_model=RelacionamentoResponse,
    include_in_schema=True,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': RelacionamentoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de questinário de relacionamento',
                            'description': 'Valores de inteiros devem ser entre 0 e 5',
                            'value': {
                                'atleta_id': 10,
                                'receptividade_contrato': 5,
                                'satisfacao_empresa': 3,
                                'satisfacao_clube': 4,
                                'relacao_familiares': 5,
                                'influencias_externas': 2,
                                'pendencia_empresa': 'true',
                                'pendencia_clube': 'true',
                                'data_avaliacao': '2024-01-01',
                            },
                        }
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/clube/atleta/{id}',
    endpoint=clube,
    methods=['GET'],
    include_in_schema=True,
)


def init_app(app):
    app.include_router(router)
