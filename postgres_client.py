import os
import psycopg2

def get_dtc_info(code):
    """
    Fetch DTC details from PostgreSQL table `obd_codes`.
    Required columns:
      code, description, causes, fixes, severity
    """
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()

        cur.execute("""
            SELECT code, tcode, sections
            FROM obd_codes
            WHERE code = %s;
        """, (code,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return None

        return {
            "code": row[0],
            "tcode": row[1],
            "sections": row[2]
        }

    except Exception as e:
        print(f"[get_dtc_info] ERROR: {e}")
        return None
