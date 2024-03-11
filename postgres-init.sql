CREATE TABLE IF NOT EXISTS public.important_data (
    name text unique not null primary key,
    value text null
);

INSERT INTO important_data (name, value) VALUES ('passwords', 'Your princess is in another castle!') ON CONFLICT DO NOTHING;
INSERT INTO important_data (name, value) VALUES ('actual_passwords', 'Got me there') ON CONFLICT DO NOTHING;
