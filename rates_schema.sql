CREATE DATABASE currencies;

\c currencies;

CREATE TABLE daily_rates (
  day DATE,
  rates JSON
);
