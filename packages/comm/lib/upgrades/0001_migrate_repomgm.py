# encoding: utf-8
"""Migrazione delle tabelle `repomgm` verso i nuovi package `github` e `sbs`.

Nota: le tabelle sorgente potrebbero non essere più nel model o avere nomi
prefissati (es. public.repomgm_repository). Le individuiamo direttamente dal DB.
"""


def table_exists(db, full_name):
    """
    True se la tabella esiste in DB (anche se non è più nel model),
    False altrimenti.
    """
    res = db.execute("SELECT to_regclass(:tname)", dict(tname=full_name)).fetchone()
    return bool(res and res[0])


def find_table(db, preferred_names, fallback_name=None):
    """
    Restituisce il primo nome tabella esistente tra quelli preferiti.
    Se non trova nulla, prova a cercare per table_name (fallback_name).
    """
    for name in preferred_names:
        if table_exists(db, name):
            return name

    if not fallback_name:
        return None

    found = db.execute(
        """
        SELECT table_schema || '.' || table_name
        FROM information_schema.tables
        WHERE table_name=:tname
        ORDER BY table_schema
        LIMIT 1
        """,
        dict(tname=fallback_name),
    ).fetchone()
    if found:
        return found[0]
    return None


def fetch_rows(db, full_name):
    """Legge tutte le righe dalla tabella sorgente come lista di dict."""
    cursor = db.execute(f"SELECT * FROM {full_name}")
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


def migrate_table(db, source_candidates, dest_path, field_map, pkey_field="id"):
    """
    Copia le righe dalla prima tabella trovata in `source_candidates` verso `dest_path`.

    field_map è un dict {colonna_sorgente: colonna_destinazione}.
    Si inseriscono solo le righe che non esistono già (match sul pkey_field).
    """
    source = find_table(
        db,
        preferred_names=source_candidates,
        fallback_name=source_candidates[-1].split(".")[-1],
    )
    if not source:
        print(
            f"Skip {source_candidates[0]}: tabella inesistente "
            f"(cercate varianti: {', '.join(source_candidates)})"
        )
        return 0

    dest_tbl = db.table(dest_path)
    rows = fetch_rows(db, source)
    inserted = 0

    for row in rows:
        pkey = row.get(pkey_field)
        if not pkey:
            continue

        # evita duplicati se la riga è già stata migrata
        if dest_tbl.readColumns(pkey, columns=pkey_field):
            continue

        record = dest_tbl.newrecord(
            **{dst: row[src] for src, dst in field_map.items() if src in row}
        )
        record[pkey_field] = pkey
        dest_tbl.insert(record)
        inserted += 1

    db.commit()
    print(f"Migrate {source} -> {dest_path}: inserite {inserted} righe")
    return inserted


def cleanup_repomgm(db, tables):
    """Svuota le tabelle repomgm nell'ordine fornito."""
    for candidates in tables:
        source = find_table(
            db,
            preferred_names=candidates,
            fallback_name=candidates[-1].split(".")[-1],
        )
        if not source:
            continue
        db.execute(f"DELETE FROM {source}")
    db.commit()


def main(db):
    migrations = [
        (
            [
                "repomgm.git_organization",
                "repomgm.repomgm_git_organization",
                "public.repomgm_git_organization",
                "public.repomgm.repomgm_git_organization",
            ],
            "github.organization",
            {"id": "id", "code": "code", "description": "description"},
        ),
        (
            [
                "repomgm.repository",
                "repomgm.repomgm_repository",
                "public.repomgm_repository",
                "public.repomgm.repomgm_repository",
            ],
            "github.repository",
            {
                "id": "id",
                "code": "code",
                "title": "title",
                "logo": "logo",
                "description": "description",
                "organization_id": "organization_id",
                "metadata": "metadata",
            },
        ),
        (
            [
                "repomgm.frequency",
                "repomgm.repomgm_frequency",
                "public.repomgm_frequency",
                "public.repomgm.repomgm_frequency",
            ],
            "sbs.frequency",
            {
                "code": "code",
                "description": "description",
                "days_for_renewal": "days_for_renewal",
            },
            "code",
        ),
        (
            [
                "repomgm.subscription_plan",
                "repomgm.repomgm_subscription_plan",
                "public.repomgm_subscription_plan",
                "public.repomgm.repomgm_subscription_plan",
            ],
            "sbs.subscription_plan",
            {
                "id": "id",
                "repository_id": "repository_id",
                "description": "description",
                "full_description": "full_description",
                "price": "price",
                "currency": "currency",
                "frequency_code": "frequency_code",
                "start_date": "start_date",
                "end_date": "end_date",
                "enable_subscription": "enable_subscription",
            },
        ),
        (
            [
                "repomgm.subscription",
                "repomgm.repomgm_subscription",
                "public.repomgm_subscription",
                "public.repomgm.repomgm_subscription",
            ],
            "sbs.subscription",
            {
                "id": "id",
                "user_id": "user_id",
                "repository_id": "repository_id",
                "subscription_plan_id": "subscription_plan_id",
                "role_id": "role_id",
                "start_date": "start_date",
                "end_date": "end_date",
                "permission_level": "permission_level",
            },
        ),
    ]

    for source_candidates, dest, field_map, *pkey in migrations:
        migrate_table(db, source_candidates, dest, field_map, pkey[0] if pkey else "id")

    cleanup_repomgm(
        db,
        [
            [
                "repomgm.subscription",
                "repomgm.repomgm_subscription",
                "public.repomgm_subscription",
                "public.repomgm.repomgm_subscription",
            ],
            [
                "repomgm.subscription_plan",
                "repomgm.repomgm_subscription_plan",
                "public.repomgm_subscription_plan",
                "public.repomgm.repomgm_subscription_plan",
            ],
            [
                "repomgm.repository",
                "repomgm.repomgm_repository",
                "public.repomgm_repository",
                "public.repomgm.repomgm_repository",
            ],
            [
                "repomgm.git_organization",
                "repomgm.repomgm_git_organization",
                "public.repomgm_git_organization",
                "public.repomgm.repomgm_git_organization",
            ],
            [
                "repomgm.frequency",
                "repomgm.repomgm_frequency",
                "public.repomgm_frequency",
                "public.repomgm.repomgm_frequency",
            ],
        ],
    )
