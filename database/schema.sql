-- =====================================================
-- Nepal Flood Risk Intelligence System
-- Database Schema
-- =====================================================

DROP TABLE IF EXISTS subscriptions CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS model_predictions CASCADE;
DROP TABLE IF EXISTS engineered_features CASCADE;
DROP TABLE IF EXISTS flood_events CASCADE;
DROP TABLE IF EXISTS discharge_daily CASCADE;
DROP TABLE IF EXISTS weather_daily CASCADE;
DROP TABLE IF EXISTS districts CASCADE;

-- =====================================================
-- Districts
-- =====================================================

CREATE TABLE districts (
    district_id SERIAL PRIMARY KEY,
    district_name VARCHAR(100) UNIQUE NOT NULL,

    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    elevation_m DOUBLE PRECISION
);

-- =====================================================
-- Weather Data (NASA + Daily API)
-- =====================================================

CREATE TABLE weather_daily (
    weather_id SERIAL PRIMARY KEY,

    district_id INTEGER NOT NULL,
    record_date DATE NOT NULL,

    rainfall_mm DOUBLE PRECISION,
    temp_max_c DOUBLE PRECISION,
    temp_min_c DOUBLE PRECISION,
    humidity_pct DOUBLE PRECISION,
    wind_ms DOUBLE PRECISION,

    CONSTRAINT fk_weather_district
        FOREIGN KEY (district_id)
        REFERENCES districts(district_id),

    CONSTRAINT uq_weather
        UNIQUE (district_id, record_date)
);

-- =====================================================
-- GloFAS River Discharge
-- =====================================================

CREATE TABLE discharge_daily (
    discharge_id SERIAL PRIMARY KEY,

    district_id INTEGER NOT NULL,
    record_date DATE NOT NULL,

    discharge_m3s DOUBLE PRECISION,

    CONSTRAINT fk_discharge_district
        FOREIGN KEY (district_id)
        REFERENCES districts(district_id),

    CONSTRAINT uq_discharge
        UNIQUE (district_id, record_date)
);

-- =====================================================
-- BIPAD Flood Events
-- =====================================================

CREATE TABLE flood_events (
    event_id SERIAL PRIMARY KEY,

    district_id INTEGER NOT NULL,

    event_date DATE NOT NULL,

    title TEXT,
    province VARCHAR(100),
    municipality VARCHAR(150),

    agriculture_loss_npr DOUBLE PRECISION,
    infrastructure_loss_npr DOUBLE PRECISION,

    infrastructure_destroyed INTEGER,
    houses_destroyed INTEGER,
    houses_affected INTEGER,

    livestock_destroyed INTEGER,

    deaths INTEGER,
    missing INTEGER,
    injured INTEGER,

    CONSTRAINT fk_flood_district
        FOREIGN KEY (district_id)
        REFERENCES districts(district_id)
);

-- =====================================================
-- Engineered Features
-- =====================================================

CREATE TABLE engineered_features (
    feature_id SERIAL PRIMARY KEY,

    district_id INTEGER NOT NULL,
    record_date DATE NOT NULL,

    rainfall_mm DOUBLE PRECISION,
    rainfall_3d_mm DOUBLE PRECISION,
    rainfall_7d_mm DOUBLE PRECISION,

    discharge_m3s DOUBLE PRECISION,

    days_since_last_flood INTEGER,

    elevation_risk DOUBLE PRECISION,

    fii DOUBLE PRECISION,

    risk_label VARCHAR(20),

    CONSTRAINT fk_feature_district
        FOREIGN KEY (district_id)
        REFERENCES districts(district_id)
);

-- =====================================================
-- Model Predictions
-- =====================================================

CREATE TABLE model_predictions (
    prediction_id SERIAL PRIMARY KEY,

    district_id INTEGER NOT NULL,

    prediction_date DATE NOT NULL,

    predicted_fii DOUBLE PRECISION,

    predicted_risk VARCHAR(20),

    confidence DOUBLE PRECISION,

    CONSTRAINT fk_prediction_district
        FOREIGN KEY (district_id)
        REFERENCES districts(district_id)
);

-- =====================================================
-- Users
-- =====================================================

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(255) UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Alert Subscriptions
-- =====================================================

CREATE TABLE subscriptions (
    subscription_id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    district_id INTEGER NOT NULL,

    CONSTRAINT fk_subscription_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_subscription_district
        FOREIGN KEY (district_id)
        REFERENCES districts(district_id)
);

-- =====================================================
-- New and Old District Names 
-- =====================================================

CREATE TABLE district_aliases (
    alias_id SERIAL PRIMARY KEY,

    alias_name VARCHAR(100) UNIQUE NOT NULL,

    district_id INTEGER NOT NULL,

    CONSTRAINT fk_alias_district
        FOREIGN KEY (district_id)
        REFERENCES districts(district_id)
);

CREATE TABLE IF NOT EXISTS flood_incidents (
    incident_id SERIAL PRIMARY KEY,

    district_id INTEGER NOT NULL
        REFERENCES districts(district_id),

    incident_date DATE NOT NULL,

    house_destroyed INTEGER,
    house_affected INTEGER,

    people_death INTEGER,
    people_injured INTEGER,
    people_missing INTEGER,

    agriculture_loss_npr BIGINT,
    infrastructure_loss_npr BIGINT,

    source VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS river_discharge_daily (
    discharge_id SERIAL PRIMARY KEY,

    district_id INTEGER NOT NULL
        REFERENCES districts(district_id),

    record_date DATE NOT NULL,

    discharge_m3s DOUBLE PRECISION NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(district_id, record_date)
);

CREATE TABLE IF NOT EXISTS heavy_rainfall_incidents (
    incident_id SERIAL PRIMARY KEY,

    district_id INTEGER NOT NULL
        REFERENCES districts(district_id),

    incident_date DATE NOT NULL,

    estimated_loss_npr NUMERIC(14,2),

    house_destroyed INTEGER,
    house_affected INTEGER,

    livestock_destroyed INTEGER,

    people_death INTEGER,
    people_missing INTEGER,
    people_injured INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_heavy_rainfall_date
ON heavy_rainfall_incidents(incident_date);

CREATE INDEX idx_heavy_rainfall_district
ON heavy_rainfall_incidents(district_id);

CREATE TABLE IF NOT EXISTS training_features (
    feature_id SERIAL PRIMARY KEY,

    district_id INTEGER NOT NULL,
    record_date DATE NOT NULL,

    rainfall_mm DOUBLE PRECISION,
    rainfall_3d_mm DOUBLE PRECISION,
    rainfall_7d_mm DOUBLE PRECISION,

    temp_max_c DOUBLE PRECISION,
    temp_min_c DOUBLE PRECISION,
    humidity_pct DOUBLE PRECISION,
    wind_ms DOUBLE PRECISION,

    discharge_m3s DOUBLE PRECISION,
    discharge_change_3d DOUBLE PRECISION,

    elevation_m DOUBLE PRECISION,

    flood_last_30d INTEGER DEFAULT 0,
    flood_last_365d INTEGER DEFAULT 0,

    heavy_rain_last_7d INTEGER DEFAULT 0,
    heavy_rain_last_30d INTEGER DEFAULT 0,

    days_since_last_flood INTEGER,

    season_encoded INTEGER,

    fii DOUBLE PRECISION,

    risk_label VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(district_id, record_date)
);