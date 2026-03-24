import random
from datetime import datetime, timedelta

# Foydalanuvchilar ma'lumotlari
USERS = [
    {
        "person_id": 20238393,
        "group_id": 20230144,
        "direction": "Vxod-orqa-1",
        "deviceName": "Vxod-orqa-1",
        "deviceSN": "e0:ca:3c:f3:1f:5c",
        "personName": "Amirov Akrom"
    },
    # {
    #     "person_id": 20238397,
    #     "group_id": 20230144,
    #     "direction": "Vxod2",
    #     "deviceName": "VXOD2",
    #     "deviceSN": "e0:ca:3c:f3:1f:5b",
    #     "personName": "Abdurahmonov Behzod"
    # },
    # {
    #     "person_id": 20238394,
    #     "group_id": 20230144,
    #     "direction": "Vxod5",
    #     "deviceName": "VXOD5",
    #     "deviceSN": "e0:ca:3c:f3:1f:60",
    #     "personName": "Eldor Isoqov"
    # },
]

def generate_sql_for_date(date_str: str, entries_per_user: int = 2):
    """
    Har bir foydalanuvchi uchun date_str kunida tasodifiy vaqtli INSERT yaratadi
    :param date_str: Sana (masalan: "2025-09-22")
    :param entries_per_user: nechta yozuv per user
    """
    base_date = datetime.strptime(date_str, "%Y-%m-%d")
    results = []

    for user in USERS:
        for _ in range(entries_per_user):
            # Random vaqt oralig'i: 08:50 dan 09:15 gacha
            start_time = datetime.combine(base_date, datetime.strptime("08:50:00", "%H:%M:%S").time())
            end_time = datetime.combine(base_date, datetime.strptime("09:20:00", "%H:%M:%S").time())
            rand_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
            rand_dt = start_time + timedelta(seconds=rand_seconds)

            date_full = rand_dt.strftime("%Y-%m-%d %H:%M:%S")
            sana = rand_dt.strftime("%Y-%m-%d")
            vaqt = rand_dt.strftime("%H:%M:%S")
            iso_time = rand_dt.strftime("%Y-%m-%dT%H:%M:%S+05:00")
            unix_time = int(rand_dt.timestamp())

            sql = f"""INSERT INTO tbl_davomat (person_id, date, group_id, sana, vaqt, direction, deviceName, deviceSN, personName, cardNo, timecontrol) VALUES (
                        {user["person_id"]},
                        '{date_full}',
                        {user["group_id"]},
                        '{sana}',
                        '{vaqt}',
                        '{user["direction"]}',
                        '{user["deviceName"]}',
                        '{user["deviceSN"]}',
                        '{user["personName"]}',
                        '{iso_time}',
                        {unix_time}
                        );"""
            results.append(sql.strip())
    return "\n\n".join(results)


# === Ishlatish ===
if __name__ == "__main__":
    sana = "2026-01-26"   # siz faqat bitta sanani kiritasiz
    print(generate_sql_for_date( sana))
