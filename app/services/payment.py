import logging
from decimal import Decimal
from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.payment import Payment, PaymentStatus
from ..models.membership import Membership, MembershipStatus
from ..schemas.payment import PaymentCreate, PaymentUpdate
from datetime import datetime

logger = logging.getLogger("gymapi")


class PaymentService:

    @staticmethod
    def get_all(session: Session, status=None, method=None, membership_id=None,
                skip: int = 0, limit: int = 20) -> list[Payment]:
        q = select(Payment)
        if status:
            q = q.where(Payment.status == status)
        if method:
            q = q.where(Payment.payment_method == method)
        if membership_id:
            q = q.where(Payment.membership_id == membership_id)
        return session.exec(q.order_by(Payment.payment_date.desc()).offset(skip).limit(limit)).all()

    @staticmethod
    def get_by_id(session: Session, payment_id: int) -> Payment:
        p = session.get(Payment, payment_id)
        if not p:
            raise HTTPException(status_code=404, detail="Payment not found")
        return p

    @staticmethod
    def create(session: Session, data: PaymentCreate) -> Payment:
        membership = session.get(Membership, data.membership_id)
        if not membership:
            raise HTTPException(status_code=404, detail="Membership not found")
        if membership.status == MembershipStatus.cancelled:
            raise HTTPException(status_code=400, detail="Cannot register payments on cancelled memberships")
        
        payment = Payment.model_validate(data)
        session.add(payment)
        session.flush()
        
        if payment.status == PaymentStatus.completed and membership.status == MembershipStatus.pending:
            # Query existing completed payments, excluding the current one to prevent double-counting if flushed
            previous_payments = session.exec(
                select(Payment).where(
                    Payment.membership_id == membership.id,
                    Payment.status == PaymentStatus.completed,
                    Payment.id != payment.id
                )
            ).all()
            
            total = sum(p.amount for p in previous_payments) + payment.amount
            
            from ..models.plan import Plan
            plan = session.get(Plan, membership.plan_id)
            
            if plan and total >= plan.price:
                membership.status = MembershipStatus.active
                membership.updated_at = datetime.utcnow()
                session.add(membership)
                logger.info(f"Membership {membership.id} automatically activated via full payment")
                
        session.commit()
        session.refresh(payment)
        return payment

    @staticmethod
    def export_csv(session: Session) -> list[dict]:
        payments = session.exec(select(Payment)).all()
        rows = []
        for p in payments:
            membership = session.get(Membership, p.membership_id)
            from ..models.member import Member
            from ..models.plan import Plan
            member = session.get(Member, membership.member_id) if membership else None
            plan = session.get(Plan, membership.plan_id) if membership else None
            rows.append({
                "id": p.id,
                "member": member.full_name if member else "",
                "plan": plan.name if plan else "",
                "amount": str(p.amount),
                "payment_method": p.payment_method.value,
                "status": p.status.value,
                "reference": p.reference,
                "payment_date": p.payment_date.strftime("%d/%m/%Y %H:%M"),
            })
        return rows