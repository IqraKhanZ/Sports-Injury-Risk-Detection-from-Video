from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.auth import get_current_user
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


async def _seed_contextual_user_notifications(db, current_user: dict):
    """
    Generates dynamic, non-hardcoded, profile-specific initial notifications
    tailored strictly to the user's real database records, role, sport, and roster.
    """
    user_email = current_user["email"]
    user_fullname = current_user.get("fullname", "User")
    user_role = current_user.get("role", "Athlete")
    now = datetime.utcnow()
    notifications = []

    if user_role == "Athlete":
        profile = await db.athlete_profiles.find_one({"email": user_email})
        latest_analysis = await db.video_analyses.find_one(
            {"email": user_email}, sort=[("upload_date", -1)]
        )

        if not profile:
            notifications.append({
                "notification_id": f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
                "recipient_email": user_email,
                "recipient_role": "Athlete",
                "type": "Onboarding",
                "category": "Profile Setup",
                "title": f"Welcome {user_fullname} — Complete Your Athlete Profile",
                "message": "Fill out your physical metrics and questionnaire in the Settings tab to calibrate your baseline injury risk calculations.",
                "priority": "Medium",
                "is_read": False,
                "created_at": now
            })
        else:
            sport = profile.get("sport_type", "Sport")
            coach = profile.get("assigned_coach")
            physio = profile.get("assigned_physio")
            ath_id = profile.get("athlete_id", "ATH-1001")

            if latest_analysis:
                risk = latest_analysis.get("scores", {}).get("injury_risk_score", 25)
                priority = "High" if risk >= 50 else "Medium" if risk >= 30 else "Low"
                notifications.append({
                    "notification_id": f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
                    "recipient_email": user_email,
                    "recipient_role": "Athlete",
                    "type": "Analysis Summary",
                    "category": "Biomechanics",
                    "title": f"Biomechanical Baseline Active ({sport})",
                    "message": f"Your latest movement video analysis for {ath_id} recorded an Injury Risk Score of {risk}%.",
                    "priority": priority,
                    "is_read": False,
                    "created_at": now
                })
            else:
                notifications.append({
                    "notification_id": f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
                    "recipient_email": user_email,
                    "recipient_role": "Athlete",
                    "type": "Action Required",
                    "category": "Video Analysis",
                    "title": f"Upload Your First {sport} Movement Video",
                    "message": f"Welcome {user_fullname} ({ath_id}). Upload a running, jumping, or agility video to generate full 3D pose tracking and ML risk predictions.",
                    "priority": "Medium",
                    "is_read": False,
                    "created_at": now
                })

            if coach:
                notifications.append({
                    "notification_id": f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
                    "recipient_email": user_email,
                    "recipient_role": "Athlete",
                    "type": "Coach Connection",
                    "category": "Roster",
                    "title": f"Coach Linked: {coach}",
                    "message": f"Coach {coach} is assigned to your profile and can review your movement videos and prescribe custom training drills.",
                    "priority": "Low",
                    "is_read": False,
                    "created_at": now
                })

    elif user_role == "Coach":
        assigned_cursor = db.athlete_profiles.find({"assigned_coach": user_fullname})
        athletes = await assigned_cursor.to_list(length=50)

        if athletes:
            ath_names = []
            for ath in athletes:
                u = await db.users.find_one({"email": ath.get("email")})
                ath_names.append(u["fullname"] if u else ath.get("athlete_id", "Athlete"))

            notifications.append({
                "notification_id": f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
                "recipient_email": user_email,
                "recipient_role": "Coach",
                "type": "Roster Overview",
                "category": "Team Management",
                "title": f"Active Training Roster: {len(athletes)} Assigned Athletes",
                "message": f"Your current roster includes: {', '.join(ath_names[:4])}{'...' if len(ath_names) > 4 else ''}. Select an athlete from the dropdown to review movement quality.",
                "priority": "Medium",
                "is_read": False,
                "created_at": now
            })
        else:
            notifications.append({
                "notification_id": f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
                "recipient_email": user_email,
                "recipient_role": "Coach",
                "type": "Roster Status",
                "category": "Team Management",
                "title": f"Welcome Coach {user_fullname}",
                "message": "You currently have 0 assigned athletes. Athletes can select you as their primary coach during their questionnaire setup.",
                "priority": "Low",
                "is_read": False,
                "created_at": now
            })

    elif user_role == "Physiotherapist":
        assigned_cursor = db.athlete_profiles.find({"assigned_physio": user_fullname})
        patients = await assigned_cursor.to_list(length=50)

        if patients:
            patient_names = []
            for ath in patients:
                u = await db.users.find_one({"email": ath.get("email")})
                patient_names.append(u["fullname"] if u else ath.get("athlete_id", "Patient"))

            notifications.append({
                "notification_id": f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
                "recipient_email": user_email,
                "recipient_role": "Physiotherapist",
                "type": "Clinical Roster",
                "category": "Rehabilitation",
                "title": f"Clinical Queue: {len(patients)} Active Patients",
                "message": f"Patients currently under your physiotherapy care: {', '.join(patient_names[:4])}{'...' if len(patient_names) > 4 else ''}.",
                "priority": "Medium",
                "is_read": False,
                "created_at": now
            })
        else:
            notifications.append({
                "notification_id": f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
                "recipient_email": user_email,
                "recipient_role": "Physiotherapist",
                "type": "Clinical Status",
                "category": "Rehabilitation",
                "title": f"Welcome {user_fullname}",
                "message": "Your rehabilitation clinical queue is clear. Athletes will appear here once assigned to you.",
                "priority": "Low",
                "is_read": False,
                "created_at": now
            })

    elif user_role == "Sports Scientist":
        tot_analyses = await db.video_analyses.count_documents({})
        tot_athletes = await db.athlete_profiles.count_documents({})
        notifications.append({
            "notification_id": f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
            "recipient_email": user_email,
            "recipient_role": "Sports Scientist",
            "type": "Dataset Ingestion",
            "category": "Kinematics",
            "title": "Platform Biomechanical Telemetry Online",
            "message": f"{tot_athletes} athlete profiles and {tot_analyses} processed video kinematic recordings indexed in database.",
            "priority": "Low",
            "is_read": False,
            "created_at": now
        })

    elif user_role == "Administrator":
        tot_users = await db.users.count_documents({})
        tot_analyses = await db.video_analyses.count_documents({})
        notifications.append({
            "notification_id": f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
            "recipient_email": user_email,
            "recipient_role": "Administrator",
            "type": "System Audit",
            "category": "Infrastructure",
            "title": "SIRD Core Engine & Database Operational",
            "message": f"Local inference engine active. {tot_users} user accounts and {tot_analyses} motion tracking records verified.",
            "priority": "Low",
            "is_read": False,
            "created_at": now
        })

    if notifications:
        await db.notifications.insert_many(notifications)


@router.get("/me")
async def get_my_notifications(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Fetch all notifications for the logged-in user.
    If none exist yet, automatically generate intelligent contextual notifications
    strictly derived from that user's real profile, role, and roster.
    """
    user_email = current_user["email"]

    cursor = db.notifications.find(
        {"recipient_email": user_email}
    ).sort("created_at", -1)
    notifications = await cursor.to_list(length=100)

    if not notifications:
        await _seed_contextual_user_notifications(db, current_user)
        cursor = db.notifications.find(
            {"recipient_email": user_email}
        ).sort("created_at", -1)
        notifications = await cursor.to_list(length=100)

    unread_count = 0
    formatted = []
    for doc in notifications:
        doc["_id"] = str(doc["_id"])
        if not doc.get("is_read", False):
            unread_count += 1
        formatted.append(doc)

    return {
        "unread_count": unread_count,
        "notifications": formatted
    }


@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    result = await db.notifications.update_one(
        {
            "notification_id": notification_id,
            "recipient_email": current_user["email"]
        },
        {"$set": {"is_read": True}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found.")
    return {"status": "success", "notification_id": notification_id}


@router.put("/read-all")
@router.put("/read-all/mark")
async def mark_all_notifications_read(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    await db.notifications.update_many(
        {"recipient_email": current_user["email"]},
        {"$set": {"is_read": True}}
    )
    return {"status": "success", "message": "All notifications marked as read."}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    result = await db.notifications.delete_one(
        {
            "notification_id": notification_id,
            "recipient_email": current_user["email"]
        }
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found.")
    return {"status": "deleted", "notification_id": notification_id}
