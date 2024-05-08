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

        filters: dict = {'page': 1, 'per_page': 1000, 'model': 'fisico'}

        atleta = self._get_atleta(atleta_id)
        
        _, clubes = self.clube_repository.list_clube(atleta_id, filters)
        _, lesoes = self.lesao_repository.list_lesao(atleta_id, filters)
        _, controles = self.controle_repository.list_controle(atleta_id, filters)
        _, competicoes = self.competicao_repository.list_competicao(atleta_id, filters)
        _, observacoes = self.observacao_repository.list_observacao(atleta_id, filters)
        _, relacionamentos = self.relacionamento_repository.list_relacionamento(atleta_id, filters)
        _, caracteristicas_fisicas, _ = (self.caracteristica_repository.list_caracteristica(atleta_id, filters))

        filters.update({'model': atleta.get('posicao_primaria')})
        _, caracteristicas_posicao, _ = (self.caracteristica_repository.list_caracteristica(atleta_id, filters))

        data = {
            'atleta': atleta,
            'clube': clubes,
            'lesao': lesoes,
            'controle': controles,
            'competicao': competicoes,
            'observacao': observacoes,
            'relacionamento': relacionamentos,
            'caracteristicas_fisicas': caracteristicas_fisicas,
            'caracteristicas_posicao': caracteristicas_posicao,
        }

        return data
    
    def _get_atleta(self, atleta_id: int) -> dict:
        atleta = self.atleta_repository.get_atleta(atleta_id)

        if atleta is not None:
            return atleta

        raise NotFoundError('Atleta não encontrado')
