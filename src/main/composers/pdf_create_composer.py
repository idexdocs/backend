from src.presentation.controllers.pdf_create import PdfCreateController
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_caracteristicas import CaracteristicasRepo
from src.repository.repo_clube import ClubeRepo
from src.repository.repo_competicao import CompeticaoRepo
from src.repository.repo_controle import ControleRepo
from src.repository.repo_lesao import LesaoRepo
from src.repository.repo_observacao import ObservacaoRepo
from src.repository.repo_relacionamento import RelacionamentoRepo
from src.use_cases.pdf_create import PdfCreateUseCase


def pdf_create_composer():
    atleta_repository = AtletaRepo()
    caracteristica_repository = CaracteristicasRepo()
    relacionamento_repository = RelacionamentoRepo()
    clube_repository = ClubeRepo()
    competicao_repository = CompeticaoRepo()
    lesao_repository = LesaoRepo()
    controle_repository = ControleRepo()
    observacao_repository = ObservacaoRepo()

    use_case = PdfCreateUseCase(
        atleta_repository=atleta_repository,
        caracteristica_repository=caracteristica_repository,
        relacionamento_repository=relacionamento_repository,
        clube_repository=clube_repository,
        competicao_repository=competicao_repository,
        lesao_repository=lesao_repository,
        controle_repository=controle_repository,
        observacao_repository=observacao_repository,
    )
    controller = PdfCreateController(use_case=use_case)

    return controller.handle
