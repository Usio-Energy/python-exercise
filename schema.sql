CREATE TABLE IF NOT EXISTS response (
    success boolean NOT NULL,
    timestamp integer NOT NULL,
    base char(3) NOT NULL,
    date date NOT NULL,
    rates jsonb NOT NULL
);
