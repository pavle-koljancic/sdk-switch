from datetime import datetime
from typing import Annotated
from typing import ClassVar

from pydantic import BeforeValidator
from pydantic import ConfigDict
from pydantic import PlainSerializer

from models.db_nso.db_base_entity import DbBaseEntity
from models.db_nso.db_base_entity import convert_str_to_datetime
from models.db_nso.db_base_entity import serialize_date_time_to_str


class DomOrdiniBeaEntity(DbBaseEntity):
    model_config = ConfigDict(frozen=True)

    id_fattibilita: str | None = None
    codice_ordine: str | None = None
    data_creazione: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    nome_operatore: str | None = None
    tipo_di_contratto: str | None = None
    prime_contractor: str | None = None
    comune_sede: str | None = None
    indirizzo_sede: str | None = None
    civico_sede: str | None = None
    area_territoriale: str | None = None
    tipo_collegamento: str | None = None
    nome_circuito: str | None = None
    stato: str | None = None
    impresa: str | None = None
    tecnico_di_progettazione: str | None = None
    assistente_operativo: str | None = None
    provincia_sede: str | None = None
    motivo_cambio_data_attivazione: str | None = None
    richiesta_sopralluogo: str | None = None
    data_primo_sopralluogo: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    data_secondo_sopralluogo: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    data_conferma_collaudo: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    data_fine_lavori: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    data_rilascio: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    data_richiesta_attivazione: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    subcontractor: str | None = None
    data_fine_progettazione: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    id_sede_crm: str | None = None
    dac: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    ultimo_cambio_stato: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    cluster: str | None = None
    convenzione: str | None = None
    esito_fattibilita: str | None = None
    note_ordine: str | None = None
    note_circuito: str | None = None
    nome_sede: str | None = None
    nome_cliente: str | None = None
    note_da_olo: str | None = None
    note_per_olo: str | None = None
    regione_sede: str | None = None
    stato_sede: str | None = None
    data_appuntamento: Annotated[
        datetime | None,
        BeforeValidator(convert_str_to_datetime),
        PlainSerializer(func=serialize_date_time_to_str, return_type=str, when_used="unless-none"),
    ] = None
    fascia_appuntamento: str | None = None
    odl: str | None = None
    stato_odl: str | None = None
    svlan_id: str | None = None
    pop_raccolta: str | None = None
    nome_kit_consegna: str | None = None
    pop_consegna: str | None = None
    nome_apparato: str | None = None
    scheda: str | None = None
    porta: str | None = None
    ip_management: str | None = None
    vlan_mgmt: str | None = None
    banda_richiesta: str | None = None
    distanza_pop_raccolta: str | None = None
    svlan_olo: str | None = None

    table_name: ClassVar[str] = "nso.dom_ordini_bea"
