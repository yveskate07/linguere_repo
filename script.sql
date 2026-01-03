/*INSERT INTO "Services_service" (name, description_accueil, description, slug)
SELECT
    name,
    description_accueil,
    description,
    slug
FROM json_to_recordset(
    pg_read_file('/Json_files/services.json')::json
) AS t(
    name TEXT,
    description_accueil TEXT,
    description TEXT,
    slug TEXT
);

DROP TABLE IF EXISTS tmp_services;

CREATE TEMP TABLE tmp_services (
    data jsonb
);

\copy tmp_services(data) FROM '/home/yveskate/projets/AntaBackEnd/Json_files/services_fields.json';

INSERT INTO "Services_fieldforservice" (id, html_field, grouped, header_icon_class, header_icon_txt, is_support_field, service_id)
SELECT
    (item->>'id')::int,
    item->>'html_field',
    (item->>'grouped')::boolean,
    item->>'header_icon_class',
    item->>'header_icon_txt',
    (item->>'is_support_field')::boolean,
    NULLIF(item->>'service_id','')::int
FROM tmp_services,
     jsonb_array_elements(data) AS item;


-- Charger le JSON proprement (multiligne, HTML-safe)
\set json `cat /home/yveskate/projets/AntaBackEnd/Json_files/services_fields.json`

DROP TABLE IF EXISTS tmp_services;

CREATE TEMP TABLE tmp_services (
    data jsonb
);

-- Insertion du JSON complet (une seule ligne)
INSERT INTO tmp_services(data)
VALUES (:'json'::jsonb);

-- Insertion dans la table finale
INSERT INTO "Services_fieldforservice"
    (id, html_field, grouped, header_icon_class, header_icon_txt, is_support_field, service_id)
SELECT
    (item->>'id')::int,
    item->>'html_field',
    (item->>'grouped')::boolean,
    item->>'header_icon_class',
    item->>'header_icon_txt',
    (item->>'is_support_field')::boolean,
    (item->>'service_id')::int
FROM tmp_services,
     jsonb_array_elements(data) AS item;*/

DROP TABLE IF EXISTS tmp_services;

CREATE TEMP TABLE tmp_services (
    data jsonb
);

-- Lecture brute du JSON (aucun échappement)
\copy tmp_services(data) FROM PROGRAM 'jq -c . /home/yveskate/projets/AntaBackEnd/Json_files/services_fields.json';

INSERT INTO "Services_fieldforservice"
    (id, html_field, grouped, header_icon_class, header_icon_txt, is_support_field, service_id)
SELECT
    (item->>'id')::int,
    item->>'html_field',
    (item->>'grouped')::boolean,
    item->>'header_icon_class',
    item->>'header_icon_txt',
    (item->>'is_support_field')::boolean,
    (item->>'service_id')::int
FROM tmp_services,
     jsonb_array_elements(data) AS item;
