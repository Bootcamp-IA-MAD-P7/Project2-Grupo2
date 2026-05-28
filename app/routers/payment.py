import csv
import io
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from ..db.session import get_session
from ..core.security import get_current_user_sub
from ..services.pago import PagoService
from ..schemas.pago import PagoCreate, PagoRead, PagoUpdate
from datetime import date

router = APIRouter(prefix="/pagos", tags=["pagos"])
auth = Depends(get_current_user_sub)


@router.get("/", response_model=list[PagoRead], summary="Listar pagos")
def listar(estado=None, metodo=None, membresia_id=None, skip: int = 0,
           limit: int = Query(20, le=100), session: Session = Depends(get_session), _=auth):
    return PagoService.get_all(session, estado=estado, metodo=metodo,
                               membresia_id=membresia_id, skip=skip, limit=limit)


@router.post("/", response_model=PagoRead, status_code=201, summary="Registrar pago")
def crear(data: PagoCreate, session: Session = Depends(get_session), _=auth):
    return PagoService.create(session, data)


@router.get("/exportar-csv", summary="Exportar historial de pagos a CSV")
def exportar_csv(session: Session = Depends(get_session), _=auth):
    rows = PagoService.exportar_csv(session)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "miembro", "plan", "monto",
                                                 "metodo_pago", "estado", "referencia", "fecha_pago"])
    writer.writeheader()
    writer.writerows(rows)
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=pagos_{date.today()}.csv"},
    )


@router.get("/{pago_id}", response_model=PagoRead, summary="Detalle pago")
def detalle(pago_id: int, session: Session = Depends(get_session), _=auth):
    return PagoService.get_by_id(session, pago_id)
