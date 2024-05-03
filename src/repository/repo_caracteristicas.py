from datetime import datetime

from sqlmodel import SQLModel, select

from .base_repo import create_session


class CaracteristicasRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_dict_from_object(
        self, result: list, model_fields: list, model_name: str
    ) -> list[dict]:

        # Determina os campos existentes utilizando a primeira row como amostra
        existing_fields = {
            field.name: field
            for field in model_fields
            if hasattr(result[0], field.name)
        }

        # Criar um dicionário fazendo o convertendo campos datetime para string
        dicts = []
        for row in result:
            row_dict = {}
            for field_name, field in existing_fields.items():
                value = getattr(row, field_name)
                if isinstance(value, datetime):
                    row_dict[field_name] = value.strftime('%Y-%m-%d')
                else:
                    row_dict[field_name] = value
            dicts.append(row_dict)

        return dicts, model_name

    def list_caracteristica(
        self, atleta_id: int, filters: dict, model: SQLModel
    ):
        with self.session_factory() as session:
            query = select(model).where(model.atleta_id == atleta_id)

            return self._create_dict_from_object(
                session.exec(query).all(),
                model.__table__.columns,
                model.__name__,
            )

    def create_caracteristica(self, model: SQLModel, data: dict):
        with self.session_factory() as session:
            data = model(**data)
            session.add(data)
            session.commit()
            session.refresh(data)
            return {'id': data.id}
