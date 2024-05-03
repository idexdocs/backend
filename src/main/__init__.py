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
from src.main.rest.lesao_create import lesao_create
from src.main.rest.lesao_list import lesao
from src.main.rest.observacao_create import observacao_create
from src.main.rest.observacao_list import observacao
from src.main.rest.relacionamento_create import relacionamento_create
from src.main.rest.relacionamento_list import relacionamento
from src.schemas.atleta import AtletaCreateResponse, AtletaCreateSchema
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

router = APIRouter()

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
                                    'data_nascimento': '1985-03-11',
                                    'posicao': 1,
                                    'clube_atual': 'Clube 1',
                                },
                                {
                                    'nome': 'Atleta 2',
                                    'data_nascimento': '1985-03-11',
                                    'posicao': 2,
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
                                    'posicao': 'Goleiro',
                                    'clube_atual': 'Clube 1a',
                                    'contrato': {
                                        'tipo': 'Nenhum',
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
            }
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
                                    'pendencia_empresa': 'false',
                                    'pendencia_clube': 'true',
                                    'data_criacao': '2024-05-01',
                                },
                                {
                                    'atleta_id': 1,
                                    'receptividade_contrato': 5,
                                    'satisfacao_empresa': 2,
                                    'satisfacao_clube': 4,
                                    'relacao_familiares': 5,
                                    'influencias_externas': 5,
                                    'pendencia_empresa': 'false',
                                    'pendencia_clube': 'false',
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
            }
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
            }
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
                                    'data_fim': 'null',
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
                                'posicao_id': 1,
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
            }
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
                                    'data_fim': 'null',
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
            }
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
                                'data_fim': 'null',
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
                                'atleta_id': 20,
                                'nome': 'São João',
                                'data_inicio': '2024-01-01',
                                'data_fim': 'null',
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
                                'data_fim': 'null',
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
    # response_model=Nenhum,
    openapi_extra={
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
                                    'data_atualizado': 'null',
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
    # response_model=ObservacaoCreateResponse,
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ObservacaoCreateSchema.model_json_schema(),
                    'examples': {
                        'example1': {
                            'summary': 'Exemplo de payload para criação de características físicas',
                            'value': {
                                'atleta_id': 2,
                                'tipo': 'relacionamento',
                                'descricao': 'sua obervação',
                            },
                        },
                        'example2': {
                            'summary': 'Exemplo de payload para criação de características para zagueiro',
                            'value': {
                                'atleta_id': 2,
                                'tipo': 'relacionamento',
                                'descricao': 'sua obervação',
                            },
                        },
                        'example3': {
                            'summary': 'Exemplo de payload para criação de características para lateral',
                            'value': {
                                'atleta_id': 2,
                                'tipo': 'relacionamento',
                                'descricao': 'sua obervação',
                            },
                        },
                        'example4': {
                            'summary': 'Exemplo de payload para criação de características para goleiro',
                            'value': {
                                'atleta_id': 2,
                                'tipo': 'relacionamento',
                                'descricao': 'sua obervação',
                            },
                        },
                        'example5': {
                            'summary': 'Exemplo de payload para criação de características para volante',
                            'value': {
                                'atleta_id': 2,
                                'tipo': 'relacionamento',
                                'descricao': 'sua obervação',
                            },
                        },
                        'example6': {
                            'summary': 'Exemplo de payload para criação de características para atacante',
                            'value': {
                                'atleta_id': 2,
                                'tipo': 'relacionamento',
                                'descricao': 'sua obervação',
                            },
                        },
                        'example7': {
                            'summary': 'Exemplo de payload para criação de características para meia',
                            'value': {
                                'atleta_id': 2,
                                'tipo': 'relacionamento',
                                'descricao': 'sua obervação',
                            },
                        },
                    },
                }
            },
            'required': True,
        },
    },
)


def init_app(app):
    app.include_router(router)
