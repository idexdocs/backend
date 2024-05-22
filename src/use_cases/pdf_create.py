from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_caracteristicas import CaracteristicasRepo
from src.repository.repo_clube import ClubeRepo
from src.repository.repo_competicao import CompeticaoRepo
from src.repository.repo_controle import ControleRepo
from src.repository.repo_lesao import LesaoRepo
from src.repository.repo_observacao import ObservacaoRepo
from src.repository.repo_relacionamento import RelacionamentoRepo


class PdfCreateUseCase:
    def __init__(
        self,
        *,
        atleta_repository: AtletaRepo,
        caracteristica_repository: CaracteristicasRepo,
        relacionamento_repository: RelacionamentoRepo,
        clube_repository: ClubeRepo,
        competicao_repository: CompeticaoRepo,
        lesao_repository: LesaoRepo,
        controle_repository: ControleRepo,
        observacao_repository: ObservacaoRepo,
    ) -> None:
        self.atleta_repository = atleta_repository
        self.caracteristica_repository = caracteristica_repository
        self.relacionamento_repository = relacionamento_repository
        self.clube_repository = clube_repository
        self.competicao_repository = competicao_repository
        self.lesao_repository = lesao_repository
        self.controle_repository = controle_repository
        self.observacao_repository = observacao_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())
        # Adicionando informações no filtro para gerenciar a impressão do PDF
        filters.update({'page': 1, 'per_page': 1000, 'model': 'fisico'})
        
        # Recuperando informações do atleta
        atleta = self._get_atleta(atleta_id)
        # Recuperando toads informações inerentes ao atleta
        _, clubes = self.clube_repository.list_clube(atleta_id, filters)
        _, lesoes = self.lesao_repository.list_lesao(atleta_id, filters)
        _, controles = self.controle_repository.list_controle(atleta_id, filters)
        _, competicoes = self.competicao_repository.list_competicao(atleta_id, filters)
        _, caracteristicas_fisicas, _ = (self.caracteristica_repository.list_caracteristica(atleta_id, filters))
        observacoes_desempenho = self.observacao_repository.list_observacao(atleta_id, filters={'tipo': 'desempenho'})
        observacoes_relacionamento = self.observacao_repository.list_observacao(atleta_id, filters={'tipo': 'relacionamento'})
        
        # Gerenciando permissões para disponibilizar informações sensíveis
        permissoes = filters.get('permissoes')
        # Dicionário com dados iniciais
        data = {
            'atleta': atleta,
            'clube': clubes,
            'lesao': lesoes,
            'controle': controles,
            'competicao': competicoes,
            'observacoes_relacionamento': observacoes_relacionamento,
            'observacoes_desempenho': observacoes_desempenho,
            'caracteristicas_fisicas': caracteristicas_fisicas,
        }

        if 'create_desempenho' in permissoes:
            # Recuperando informações específicas da posição do atleta
            filters.update({'model': atleta.get('posicao_primaria')})
            _, caracteristicas_posicao, _ = self.caracteristica_repository.list_caracteristica(atleta_id, filters)
            data.update({'caracteristicas_posicao': caracteristicas_posicao})

        if 'create_relacionamento' in permissoes:    
            _, relacionamentos = self.relacionamento_repository.list_relacionamento(atleta_id, filters)
            data.update({'relacionamento': relacionamentos})

        return data
    
    def _get_atleta(self, atleta_id: int) -> dict:
        atleta = self.atleta_repository.get_atleta(atleta_id)

        if atleta is not None:
            return atleta

        raise NotFoundError('Atleta não encontrado')
