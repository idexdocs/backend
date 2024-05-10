from fastapi import APIRouter

from src.main.rest.atleta_create import atleta_create
from src.main.rest.atleta_detail import atleta_detail
from src.main.rest.atleta_list import atleta
from src.main.rest.caracteristica_create import caracteristica_create
from src.main.rest.caracteristica_list import caracteristica
from src.main.rest.clube_create import clube_create
from src.main.rest.clube_list import clube
from src.main.rest.competicao_create import competicao_create
from src.main.rest.competicao_list import competicao
from src.main.rest.controle_create import controle_create
from src.main.rest.controle_list import controle
from src.main.rest.file_download import file_download
from src.main.rest.file_upload import file_upload
from src.main.rest.lesao_create import lesao_create
from src.main.rest.lesao_list import lesao
from src.main.rest.observacao_create import observacao_create
from src.main.rest.observacao_list import observacao
from src.main.rest.pdf_create import pdf_create
from src.main.rest.relacionamento_create import relacionamento_create
from src.main.rest.relacionamento_list import relacionamento
from src.main.rest.token import token
from src.main.rest.usuario_create import usuario_create
from src.main.rest.usuario_list import usuario_list
from src.schemas.atleta import AtletaCreateResponse, AtletaCreateSchema
from src.schemas.caracteristica import CaracteristicaCreateResponse
from src.schemas.clube import ClubeCreateResponse, ClubeCreateSchema
from src.schemas.competicao import (
    CompeticaoCreateResponse,
    CompeticaoCreateSchema,
)
from src.schemas.controle import (
    ControleCreateResponse,
    ControleCreateSchema,
    ControleListResponse,
)
from src.schemas.lesao import LesaoCreateResponse, LesaoCreateSchema
from src.schemas.observacao import (
    ObservacaoCreateResponse,
    ObservacaoCreateSchema,
    ObservacaoListResponse,
)
from src.schemas.relacionamento import (
    RelacionamentoCreateSchema,
    RelacionamentoResponse,
)
from src.schemas.token import Token
from src.schemas.usuario import UsuarioCreateResponse

router = APIRouter()

router.add_api_route(
    '/usuario/create',
    endpoint=usuario_create,
    response_model=UsuarioCreateResponse,
    tags=['Usuário'],
    methods=['POST'],
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para login de usuário',
                            'description': 'usuario_tipo_id: 1 - admim 2 - treinador 3 - externo',
                            'value': {
                                'nome': 'Nome completo',
                                'email': 'email@cloud.com',
                                'password': 'teste1234',
                                'usuario_tipo_id': '1',
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
    '/auth/token',
    endpoint=token,
    response_model=Token,
    tags=['Token'],
    methods=['POST'],
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para login de usuário',
                            'value': {
                                'email': 'emaill@cloud.com',
                                'password': 'teste1234',
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
    '/atleta',
    endpoint=atleta,
    tags=['Atleta'],
    methods=['GET'],
    openapi_extra={
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Controle',
                            'data': [
                                {
                                    'nome': 'Atleta 1',
                                    'data_nascimento': '1980-09-21',
                                    'posicao_primaria': 'atacante',
                                    'posicao_secundaria': 'meia',
                                    'posicao_terciaria': None,
                                    'clube_atual': 'Clube 1',
                                },
                                {
                                    'nome': 'Atleta 2',
                                    'data_nascimento': '1985-03-11',
                                    'posicao_primaria': 'Goleiro',
                                    'posicao_secundaria': None,
                                    'posicao_terciaria': None,
                                    'clube_atual': 'Clube 1a',
                                },
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'Não existem atletas cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
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
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
    },
)
router.add_api_route(
    '/atleta/{id}',
    endpoint=atleta_detail,
    tags=['Atleta'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 1,
                            'type': 'Atleta',
                            'data': {
                                'count': 1,
                                'type': 'Atleta',
                                'data': {
                                    'nome': 'Atleta 1',
                                    'data_nascimento': '1985-03-11',
                                    'posicao_primaria': 'atacante',
                                    'posicao_secundaria': 'meia',
                                    'posicao_terciaria': None,
                                    'clube_atual': 'Clube 1a',
                                    'contrato': {
                                        'tipo': 'Amador',
                                        'data_inicio': '2024-03-23',
                                        'data_termino': '2025-04-23',
                                    },
                                },
                            },
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'Atleta não encontrado',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/questionario/relacionamento/atleta/{id}',
    endpoint=relacionamento,
    tags=['Relacionamento'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Relacionamento',
                            'data': [
                                {
                                    'atleta_id': 1,
                                    'receptividade_contrato': 5,
                                    'satisfacao_empresa': 1,
                                    'satisfacao_clube': 2,
                                    'relacao_familiares': 3,
                                    'influencias_externas': 4,
                                    'pendencia_empresa': False,
                                    'pendencia_clube': True,
                                    'data_criacao': '2024-05-01',
                                },
                                {
                                    'atleta_id': 1,
                                    'receptividade_contrato': 5,
                                    'satisfacao_empresa': 2,
                                    'satisfacao_clube': 4,
                                    'relacao_familiares': 5,
                                    'influencias_externas': 5,
                                    'pendencia_empresa': False,
                                    'pendencia_clube': False,
                                    'data_criacao': '2024-06-05',
                                },
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui questionários cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/competicao/atleta/{id}',
    endpoint=competicao,
    tags=['Competição'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Relacionamento',
                            'data': {
                                'count': 2,
                                'type': 'Relacionamento',
                                'data': [
                                    {
                                        'nome': 'Competição 1',
                                        'data_competicao': '2022-03-01',
                                        'jogos_completos': 5,
                                        'jogos_parciais': 2,
                                        'minutagem': 320,
                                        'gols': 8,
                                    },
                                    {
                                        'nome': 'Competição 2',
                                        'data_competicao': '2022-04-01',
                                        'jogos_completos': 7,
                                        'jogos_parciais': 4,
                                        'minutagem': 375,
                                        'gols': 8,
                                    },
                                ],
                            },
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui competições cadastradas',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/lesao/atleta/{id}',
    endpoint=lesao,
    tags=['Lesão'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Clubes',
                            'data': [
                                {
                                    'nome': 'Clube A',
                                    'data_inicio': '2023-01-01',
                                    'data_fim': '2023-01-01',
                                },
                                {
                                    'nome': 'Clube B',
                                    'data_inicio': '2023-01-01',
                                    'data_fim': None,
                                },
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui controles cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/atleta',
    endpoint=atleta_create,
    tags=['Atleta'],
    methods=['POST'],
    response_model=AtletaCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': AtletaCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de atleta',
                            # 'description': 'Valores de preço deve ser no formato 300.00',
                            'value': {
                                'nome': 'Janjão',
                                'data_nascimento': '1985-03-11',
                                'clube': {
                                    'nome': 'Siga Maré',
                                    'data_inicio': '2024-05-01',
                                },
                                'contrato': {
                                    'tipo_id': 1,
                                    'data_inicio': '2024-05-01',
                                    'data_fim': '2024-05-01',
                                },
                                'posicao_primaria': 'atacante',
                                'posicao_secundaria': 'volante',
                                'posicao_terciaria': None,
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
    '/questionario/relacionamento/create',
    endpoint=relacionamento_create,
    tags=['Relacionamento'],
    methods=['POST'],
    response_model=RelacionamentoResponse,
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
                                'pendencia_empresa': True,
                                'pendencia_clube': True,
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
    tags=['Clube'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Clubes',
                            'data': [
                                {
                                    'nome': 'Clube A',
                                    'data_inicio': '2023-01-01',
                                    'data_fim': '2023-01-01',
                                },
                                {
                                    'nome': 'Clube B',
                                    'data_inicio': '2023-01-01',
                                    'data_fim': None,
                                },
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui controles cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/controle',
    endpoint=controle_create,
    tags=['Controle'],
    methods=['POST'],
    response_model=ControleCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ControleCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de controle',
                            'description': 'Valores de preço deve ser no formato 300.00',
                            'value': {
                                'atleta_id': 10,
                                'nome': 'Chuteira',
                                'quantidade': 2,
                                'preco': 499.00,
                                'data_controle': '2024-01-01',
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
    '/controle/atleta/{id}',
    endpoint=controle,
    tags=['Controle'],
    methods=['GET'],
    response_model=ControleListResponse,
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Controle',
                            'data': [
                                {
                                    'atleta_id': 3,
                                    'nome': 'Chuteira',
                                    'quantidade': 2,
                                    'preco': 49.0,
                                    'data_controle': '2024-01-01',
                                },
                                {
                                    'atleta_id': 4,
                                    'nome': 'Luva',
                                    'quantidade': 2,
                                    'preco': 30.0,
                                    'data_controle': '2024-01-01',
                                },
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui controles cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/clube',
    endpoint=clube_create,
    tags=['Clube'],
    methods=['POST'],
    response_model=ClubeCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ClubeCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de clube',
                            'description': 'Caso seja o clube atual não insesir data_fim',
                            'value': {
                                'atleta_id': 20,
                                'nome': 'São João',
                                'data_inicio': '2024-01-01',
                                'data_fim': None,
                            },
                        }
                    },
                }
            },
            'required': True,
        },
        'responses': {
            '409': {
                'description': 'Conflict',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'Conflict',
                                    'message': 'O atleta já possui clube ativo',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/lesao',
    endpoint=lesao_create,
    tags=['Lesão'],
    methods=['POST'],
    response_model=LesaoCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': LesaoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de clube',
                            'description': 'Caso seja o clube atual não insesir data_fim',
                            'value': {
                                'atleta_id': 1,
                                'descricao': 'Entorse de tornozelo esquerdo',
                                'data_lesao': '2024-01-01'
                            },
                        }
                    },
                }
            },
            'required': True,
        },
        'responses': {
            '409': {
                'description': 'Conflict',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'Conflict',
                                    'message': 'O atleta já possui clube ativo',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/competicao',
    endpoint=competicao_create,
    tags=['Competição'],
    methods=['POST'],
    response_model=CompeticaoCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': CompeticaoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de competição',
                            'value': {
                                'atleta_id': 20,
                                'nome': 'São João',
                                'data_inicio': '2024-01-01',
                                'data_fim': None,
                            },
                        }
                    },
                }
            },
            'required': True,
        },
        'responses': {
            '409': {
                'description': 'Conflict',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'Conflict',
                                    'message': 'O atleta já possui clube ativo',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/observacao',
    endpoint=observacao_create,
    tags=['Observação'],
    methods=['POST'],
    response_model=ObservacaoCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ObservacaoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de observação',
                            'value': {
                                'atleta_id': 2,
                                'tipo': 'relacionamento',
                                'descricao': 'sua obervação',
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
    '/observacao/atleta/{id}',
    endpoint=observacao,
    tags=['Observação'],
    methods=['GET'],
    response_model=ObservacaoListResponse,
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 2,
                            'type': 'Observação',
                            'data': [
                                {
                                    'atleta_id': 3,
                                    'tipo': 'relacionamento',
                                    'descricao': 'sua observação',
                                    'data_observacao': '2024-01-01',
                                },
                                {
                                    'atleta_id': 3,
                                    'tipo': 'desempenho',
                                    'descricao': 'sua observação',
                                    'data_observacao': '2024-03-01',
                                },
                                {
                                    'atleta_id': 3,
                                    'tipo': 'desempenho',
                                    'descricao': 'sua observação foi editada no dia seguinte',
                                    'data_observacao': '2024-03-02',
                                },
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui observações cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/caracteristica/atleta/{id}/',
    endpoint=caracteristica,
    tags=['Característica'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            },
            {
                'name': 'model',
                'in': 'query',
                'required': True,
                'description': 'Parâmetro de característica do atleta',
                'schema': {
                    'type': 'string',
                    'example': 'fisico, atacante, zagueiro, ...',
                },
            },
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 1,
                            'type': 'CaracteristicaFisica',
                            'data': [
                                {
                                    'id': 1,
                                    'estatura': 177.0,
                                    'envergadura': 183.0,
                                    'peso': 92.0,
                                    'percentual_gordura': 17.0,
                                    'data_criacao': '2024-05-03',
                                    'data_atualizado': None,
                                    'atleta_id': 1,
                                }
                            ],
                        }
                    }
                },
            },
            '404': {
                'description': 'Not found',
                'content': {
                    'text/plain': {
                        'example': {
                            'errors': [
                                {
                                    'title': 'NotFound',
                                    'message': 'O Atleta não possui características cadastrados',
                                }
                            ]
                        }
                    }
                },
            },
        },
    },
)
router.add_api_route(
    '/create/caracteristica',
    endpoint=caracteristica_create,
    tags=['Característica'],
    methods=['POST'],
    response_model=CaracteristicaCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ObservacaoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de características físicas',
                            'value': {
                                'caracteristica': 'fisico',
                                'atleta_id': 2,
                                'estatura': 170.0,
                                'envergadura': 183.0,
                                'peso': 90.0,
                                'percentual_gordura': 15.3,
                            },
                        },
                        'example2': {
                            'summary': 'Exemplo de payload para criação de características para zagueiro',
                            'value': {
                                'caracteristica': 'zagueiro',
                                'atleta_id': 2,
                                'estatura': 3,
                                'força': 3,
                                'passe_curto': 3,
                                'passe_longo': 3,
                                'jogo_aereo': 3,
                                'confronto_defensivo': 3,
                                'leitura_jogo': 3,
                                'ambidestria': 3,
                                'participacao_ofensica': 3,
                                'cabeceio_ofensivo': 3,
                                'passe_entre_linhas': 3,
                                'lideranca': 3,
                                'confianca': 3,
                                'inteligencia_tatica': 3,
                                'competitividade': 3,
                            },
                        },
                        'example3': {
                            'summary': 'Exemplo de payload para criação de características para lateral',
                            'value': {
                                'caracteristica': 'lateral',
                                'atleta_id': 2,
                                'estatura': 3,
                                'velocidade': 3,
                                'passe_curto': 3,
                                'passe_longo': 3,
                                'capacidade_aerobia': 3,
                                'fechemanento_defensivo': 3,
                                'leitura_jogo': 3,
                                'participacao_ofensiva': 3,
                                'cruzamento': 3,
                                'jogo_aereo': 3,
                                'conducao_bola': 3,
                                'lideranca': 3,
                                'confianca': 3,
                                'inteligencia_tatica': 3,
                                'competitividade': 3,
                            },
                        },
                        'example4': {
                            'summary': 'Exemplo de payload para criação de características para goleiro',
                            'value': {
                                'caracteristica': 'goleiro',
                                'atleta_id': 2,
                                'perfil': 3,
                                'maturacao': 3,
                                'agilidade': 3,
                                'velocidade_membros_superiores': 3,
                                'flexibilidade': 3,
                                'leitura_jogo': 3,
                                'jogo_com_pes': 3,
                                'organizacao_da_defesa': 3,
                                'dominio_coberturas_e_saidas': 3,
                                'lideranca': 3,
                                'coragem': 3,
                                'concentracao': 3,
                                'controle_estresse': 3,
                            },
                        },
                        'example5': {
                            'summary': 'Exemplo de payload para criação de características para volante',
                            'value': {
                                'caracteristica': 'volante',
                                'atleta_id': 2,
                                'estatura': 3,
                                'forca': 3,
                                'passe_curto': 3,
                                'capacidade_aerobia': 3,
                                'dinamica': 3,
                                'visao_espacial': 3,
                                'leitura_jogo': 3,
                                'dominio_orientado': 3,
                                'jogo_aereo_ofensivo': 3,
                                'passes_verticais': 3,
                                'finalizacao_media_distancia': 3,
                                'lideranca': 3,
                                'confianca': 3,
                                'inteligencia_tatica': 3,
                                'competitividade': 3,
                            },
                        },
                        'example6': {
                            'summary': 'Exemplo de payload para criação de características para atacante',
                            'value': {
                                'caracteristica': 'atacante',
                                'atleta_id': 2,
                                'estatura': 3,
                                'velocidade': 3,
                                'um_contra_um_ofensivo': 3,
                                'desmarques': 3,
                                'controle_bola': 3,
                                'cruzamentos': 3,
                                'finalizacao': 3,
                                'visao_espacial': 3,
                                'dominio_orientado': 3,
                                'dribles_em_diagonal': 3,
                                'leitura_jogo': 3,
                                'reacao_pos_perda': 3,
                                'criatividade': 3,
                                'capacidade_decisao': 3,
                                'inteligencia_tatica': 3,
                                'competitividade': 3,
                            },
                        },
                        'example7': {
                            'summary': 'Exemplo de payload para criação de características para meia',
                            'value': {
                                'caracteristica': 'meia',
                                'atleta_id': 2,
                                'estatura': 3,
                                'velocidade': 3,
                                'leitura_jogo': 3,
                                'desmarques': 3,
                                'controle_bola': 3,
                                'capacidade_aerobia': 3,
                                'finalizacao': 3,
                                'visao_espacial': 3,
                                'dominio_orientado': 3,
                                'dribles': 3,
                                'organizacao_acao_ofensica': 3,
                                'pisada_na_area_para_finalizar': 3,
                                'criatividade': 3,
                                'capacidade_decisao': 3,
                                'confianca': 3,
                                'inteligencia_tatica': 3,
                                'competitividade': 3,
                            },
                        },
                    },
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/file-upload/atleta/{id}',
    endpoint=file_upload,
    tags=['File'],
    methods=['POST'],
    openapi_extra={
        'requestBody': {
            'content': {
                'multipart/form-data': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'file': {
                                'type': 'string',
                                'format': 'binary',
                                'description': 'Upload an image file. Supported formats: .png, .jpeg',
                            }
                        },
                    }
                }
            }
        }
    },
)
router.add_api_route(
    '/file-download/atleta/{id}',
    endpoint=file_download,
    tags=['Arquivo'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
    },
)
router.add_api_route(
    '/create/pdf/atleta/{id}',
    endpoint=pdf_create,
    tags=['PDF'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'Identificador único do atleta',
                'schema': {'type': 'integer', 'example': 1},
            }
        ],
    },
)
router.add_api_route(
    '/usuarios',
    endpoint=usuario_list,
    tags=['Usuário'],
    methods=['GET'],
    openapi_extra={
        'parameters': [
            {
                'in': 'query',
                'name': 'page',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'per_page',
                'required': False,
                'schema': {'type': 'integer'},
            },
        ],
        'responses': {
            '200': {
                'description': 'Successful Response',
                'content': {
                    'application/json': {
                        'example': {
                            'count': 1,
                            'total': 1,
                            'type': 'Usuarios',
                            'data': [
                                {
                                    'nome': 'Igor de Freitas Cruz',
                                    'email': 'igor.freitas.cruz@icloud.com',
                                    'data_criacao': '2024-05-07',
                                    'tipo': 'admin',
                                }
                            ],
                        }
                    }
                },
            },
        },
    },
)


def init_app(app):
    app.include_router(router)
