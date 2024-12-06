import asyncio
import logging
import os
from datetime import date
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import Required, constr
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...db.utils import get_all_editors, get_all_meeting_points
from ...models.municipality import Municipality
from ...services.mock_data import get_mock_slots
from ...services.search_meetings import (
    is_same_appointment,
    search_appointments_in_optimisation_api,
    update_appointment_in_optimisation_api,
)
from ..dependencies.auth_token import verify_auth_token

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/getManagedMeetingPoints",
    response_model=List[Municipality],
    responses={
        200: {
            "description": "Récupère la liste des meeting points",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "201",
                            "name": "Mairie ANNEXE LILLE-SECLIN",
                            "longitude": 3.0348016639327,
                            "latitude": 50.549140395451,
                            "public_entry_address": "89 RUE ROGER BOUVRY",
                            "zip_code": "59113",
                            "city_name": "SECLIN",
                            "website": "https://www.ville-seclin.fr",
                            "city_logo": "https://www.ville-seclin.fr/images/logo-ville-seclin/logo_ville_de_seclin.png",
                        }
                    ]
                }
            },
        },
        "401": {
            "description": "Utilisateur non autorisé",
            "content": {
                "application/json": {"example": "X-HUB-RDV-AUTH-TOKEN header invalid"}
            },
        },
    },
    dependencies=[Depends(verify_auth_token)],
)
@limiter.limit("30/minute")
def get_managed_meeting_points(
    request: Request,
) -> Any:
    """
    Permet de récupérer la liste des meeting points.
    """

    return get_all_meeting_points()


@router.get(
    "/availableTimeSlots",
    responses={
        200: {
            "description": "Les rendez-vous disponibles pour les meeting points id ont bien été trouvés",
            "content": {
                "application/json": {
                    "example": {
                        "506": [
                            {
                                "datetime": "2022-12-19T10:00Z",
                                "callback_url": "https://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:00Z",
                            },
                            {
                                "datetime": "2022-12-19T10:20Z",
                                "callback_url": "https://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:20Z",
                            },
                            {
                                "datetime": "2022-12-19T10:40Z",
                                "callback_url": "https://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:40Z",
                            },
                            {
                                "datetime": "2022-12-19T11:00Z",
                                "callback_url": "https://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T11:00Z",
                            },
                        ],
                        "7789": [
                            {
                                "datetime": "2022-12-19T10:00Z",
                                "callback_url": "https://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:00Z",
                            },
                            {
                                "datetime": "2022-12-19T10:20Z",
                                "callback_url": "https://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:20Z",
                            },
                            {
                                "datetime": "2022-12-19T10:40Z",
                                "callback_url": "https://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:40Z",
                            },
                            {
                                "datetime": "2022-12-19T11:00Z",
                                "callback_url": "https://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T11:00Z",
                            },
                        ],
                    }
                }
            },
        },
        "401": {
            "description": "Utilisateur non autorisé",
            "content": {
                "application/json": {"example": "X-HUB-RDV-AUTH-TOKEN header invalid"}
            },
        },
        "404": {
            "description": "Meeting point id non trouvé",
            "content": {
                "application/json": {"example": "Unknown Meeting Point ID : 11TEST2111"}
            },
        },
    },
    dependencies=[Depends(verify_auth_token)],
)
@limiter.limit("30/minute")
async def get_available_time_slots(
    request: Request,
    meeting_point_ids: list[str] = Query(default=Required, example=["201", "203"]),
    start_date: date = Query(default=Required, example="2022-11-01"),
    end_date: date = Query(default=Required, example="2022-11-30"),
    reason: str = Query(default="CNI", enum=["CNI", "PASSPORT", "CNI-PASSPORT"]),
    documents_number: int = Query(default=1),
):
    """
    Récupère les rendez-vous disponibles sur une période donnée pour une liste de meeting point id.
    <br>
    Attention: L'heure qui sera affichée est l'heure exacte que l'on trouve dans la réponse.
    """

    all_points = get_all_meeting_points()

    result = {}

    meeting_points = []
    for meeting_point_id in meeting_point_ids:
        meeting_point = None
        index = 0
        while index < len(all_points):
            if meeting_point_id == all_points[index]["id"]:
                meeting_point = all_points[index]
                break
            index += 1

        if not meeting_point:
            raise HTTPException(
                status_code=404, detail=f"Unknown Meeting Point ID : {meeting_point_id}"
            )
        meeting_points.append(meeting_point)

    if os.environ.get("MOCK_EDITORS") in ["True", True]:
        for meeting_point in meeting_points:
            result[meeting_point["id"]] = get_mock_slots(
                meeting_point, start_date, end_date
            )
    else:
        editor_futures = []
        for editor in get_all_editors():
            editor_futures.append(
                asyncio.ensure_future(
                    editor.search_slots_in_editor(
                        meeting_points,
                        start_date,
                        end_date,
                        reason,
                        documents_number,
                        None,
                    )
                )
            )
        all_editor_time_slots = await asyncio.gather(*editor_futures)
        for editor_time_slots in all_editor_time_slots:
            for meeting_point_slots in editor_time_slots[0]:
                result[meeting_point_slots["id"]] = meeting_point_slots[
                    "available_slots"
                ]

    return result


@router.get(
    "/searchApplicationIds",
    responses={
        200: {
            "description": "La recherche des numéros de pré-demande a bien aboutie!",
            "content": {
                "application/json": {
                    "example": {
                        "6123155111": [
                            {
                                "meeting_point": "Mairie ANNEXE LILLE-SECLIN",
                                "datetime": "2022-12-19T10:00Z",
                                "management_url": "https://www.ville-seclin.fr/rendez-vous/predemande?num=6123155111",
                                "cancel_url": "https://www.ville-seclin.fr/rendez-vous/annulation?num=6123155111",
                            }
                        ]
                    }
                }
            },
        },
        "401": {
            "description": "Utilisateur non autorisé",
            "content": {
                "application/json": {"example": "X-HUB-RDV-AUTH-TOKEN header invalid"}
            },
        },
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"}
                }
            },
        },
    },
    dependencies=[Depends(verify_auth_token)],
)
@limiter.limit("50/minute")
async def search_application_ids(
    request: Request,
    application_ids: List[
        constr(regex=r"^([a-zA-Z0-9]{10}[,;:\-/.\s])*[a-zA-Z0-9]{10}$")
    ] = Query(default=Required, example=["6123155111", "6123155222"]),
) -> Any:
    """
    Récupère la liste des rendez-vous liés aux numéros de pré-demande donnés.
    """
    _logger = logging.getLogger("root")

    editor_futures = []
    for editor in get_all_editors():
        editor_futures.append(
            asyncio.ensure_future(editor.search_meetings(application_ids))
        )
    try:
        meetings = await asyncio.gather(*editor_futures)

        searchApplicationId_result = {}
        for editor_meetings in meetings:
            for key in editor_meetings:
                if editor_meetings[key]:
                    for _ in editor_meetings[key]:
                        if "cancel_url" in _:
                            del _["cancel_url"]

                    if key not in searchApplicationId_result:
                        searchApplicationId_result[key] = []

                    searchApplicationId_result[key] += editor_meetings[key]

        result = await search_appointments_in_optimisation_api(application_ids)
        for application_id, appointments in searchApplicationId_result.items():
            if application_id not in result:
                result[application_id] = []
            for appointment in appointments:
                already_found = False
                for opti_appointment in result[application_id]:
                    if is_same_appointment(appointment, opti_appointment):
                        already_found = True
                        break
                if not already_found:
                    result[application_id].append(appointment)
                    try:
                        await update_appointment_in_optimisation_api(
                            application_id, appointment
                        )
                        _logger.info(
                            "Data regularisation on the optimisation api : %s, %s",
                            application_id,
                            appointment,
                        )
                    except Exception as update_appointment_in_opt_exc:
                        _logger.error(
                            "Error while updating appointment in optimisation api : %s",
                            update_appointment_in_opt_exc,
                        )
                        _logger.info(
                            "Appointment : %s, %s",
                            application_id,
                            appointment,
                        )

        return result
    except Exception as search_exc:
        _logger.error("Error during search application Ids : %s", search_exc)
        raise HTTPException(status_code=500, detail="Internal server error")
