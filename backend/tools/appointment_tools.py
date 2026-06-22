# backend/tools/appointment_tools.py

from backend.db.database import SessionLocal
from backend.models.appointment import Appointment


def fetch_slots() -> dict:
    """
    Return available appointment slots.
    """

    slots = [
        "10:00 AM",
        "11:00 AM",
        "2:00 PM",
        "4:00 PM"
    ]

    return {
        "success": True,
        "message": "Available slots retrieved successfully.",
        "slots": slots
    }


def book_appointment(
        name: str,
        phone: str,
        date: str,
        time: str
) -> dict:
    """
    Book an appointment. Prevents double booking.
    """

    db = SessionLocal()

    try:
        existing = db.query(Appointment).filter(
            Appointment.date == date,
            Appointment.time == time
        ).first()

        if existing:
            return {
                "success": False,
                "message": f"Sorry, the slot on {date} at {time} is already booked. Please choose another time."
            }

        appointment = Appointment(
            name=name,
            phone=phone,
            date=date,
            time=time
        )

        db.add(appointment)
        db.commit()

        return {
            "success": True,
            "message": f"Appointment booked for {name} on {date} at {time}."
        }

    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"Failed to book appointment: {str(e)}"
        }

    finally:
        db.close()


def retrieve_appointments(
        phone: str
) -> dict:
    """
    Retrieve all appointments for a phone number.
    """

    db = SessionLocal()

    try:
        appointments = db.query(Appointment).filter(
            Appointment.phone == phone
        ).all()

        data = [
            {
                "name": a.name,
                "date": a.date,
                "time": a.time
            }
            for a in appointments
        ]

        if not data:
            return {
                "success": False,
                "message": "No appointments found for this phone number.",
                "appointments": []
            }

        return {
            "success": True,
            "message": f"Found {len(data)} appointment(s).",
            "appointments": data
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to retrieve appointments: {str(e)}",
            "appointments": []
        }

    finally:
        db.close()


def cancel_appointment(
        phone: str,
        date: str,
        time: str
) -> dict:
    """
    Cancel an appointment by phone, date, and time.
    """

    db = SessionLocal()

    try:
        appointment = db.query(Appointment).filter(
            Appointment.phone == phone,
            Appointment.date == date,
            Appointment.time == time
        ).first()

        if not appointment:
            return {
                "success": False,
                "message": "No matching appointment found to cancel."
            }

        db.delete(appointment)
        db.commit()

        return {
            "success": True,
            "message": f"Appointment on {date} at {time} has been cancelled."
        }

    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"Failed to cancel appointment: {str(e)}"
        }

    finally:
        db.close()


def modify_appointment(
        phone: str,
        old_date: str,
        old_time: str,
        new_date: str,
        new_time: str
) -> dict:
    """
    Modify an existing appointment.
    Checks for double booking on the new slot.
    """

    db = SessionLocal()

    try:
        appointment = db.query(Appointment).filter(
            Appointment.phone == phone,
            Appointment.date == old_date,
            Appointment.time == old_time
        ).first()

        if not appointment:
            return {
                "success": False,
                "message": "No matching appointment found to modify."
            }

        duplicate = db.query(Appointment).filter(
            Appointment.date == new_date,
            Appointment.time == new_time
        ).first()

        if duplicate:
            return {
                "success": False,
                "message": f"The new slot on {new_date} at {new_time} is already booked."
            }

        appointment.date = new_date
        appointment.time = new_time

        db.commit()

        return {
            "success": True,
            "message": f"Appointment rescheduled from {old_date} {old_time} to {new_date} {new_time}."
        }

    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"Failed to modify appointment: {str(e)}"
        }

    finally:
        db.close()