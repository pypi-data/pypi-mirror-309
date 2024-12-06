-- Add up migration script here
CREATE EXTENSION moddatetime;

CREATE TABLE locks (
    id uuid DEFAULT gen_random_uuid(),
    lock_name VARCHAR NOT NULL,
    creator VARCHAR,
    ip INET,
    expires_at TIMESTAMPTZ NOT NULL DEFAULT NOW() + (10 ||' minutes')::interval ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    UNIQUE(lock_name)
);

CREATE TRIGGER locks_moddatetime
    BEFORE UPDATE ON locks
    FOR EACH ROW
    EXECUTE PROCEDURE moddatetime (updated_at);
