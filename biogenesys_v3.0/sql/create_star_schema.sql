
-- #########################################
-- 1. DIMENSION TABLES (PK: location_key)
-- #########################################

-- A. Dim_Country
CREATE TABLE "Dim_Country" (
    location_key          VARCHAR(10)   NOT NULL,
    country_code          CHAR(2)       NULL,
    country_name          VARCHAR(100)  NULL,
    CONSTRAINT PK_Dim_Country PRIMARY KEY (location_key)
);

-- B. Dim_Population
CREATE TABLE "Dim_Population" (
    location_key          VARCHAR(10)   NOT NULL,
    population            BIGINT NULL,
    population_male       BIGINT NULL,
    population_female     BIGINT NULL,
    population_rural      BIGINT NULL,
    population_urban      BIGINT NULL,
    population_density    DECIMAL(10, 4) NULL,
    population_largest_city BIGINT NULL,
    population_age_10_39  BIGINT NULL,
    population_age_40_69  BIGINT NULL,
    population_age_70_plus BIGINT NULL,
    CONSTRAINT PK_Dim_Population PRIMARY KEY (location_key)
);

-- C. Dim_Geography
CREATE TABLE "Dim_Geography" (
    location_key          VARCHAR(10)   NOT NULL,
    latitude              FLOAT         NULL,
    longitude             FLOAT         NULL,
    area_sq_km            DECIMAL(18, 2) NULL,
    area_rural_sq_km      DECIMAL(18, 2) NULL,
    area_urban_sq_km      DECIMAL(18, 2) NULL,
    average_temperature_celsius DECIMAL(5, 2) NULL,
    minimum_temperature_celsius DECIMAL(5, 2) NULL,
    maximum_temperature_celsius DECIMAL(5, 2) NULL,
    rainfall_mm           DECIMAL(10, 4) NULL,
    relative_humidity     DECIMAL(6, 3)  NULL,
    CONSTRAINT PK_Dim_Geography PRIMARY KEY (location_key)
);

-- D. Dim_Health
CREATE TABLE "Dim_Health" (
    location_key          VARCHAR(10)   NOT NULL,
    nurses_per_1000       DECIMAL(5, 2)  NULL,
    physicians_per_1000   DECIMAL(5, 2)  NULL,
    smoking_prevalence    DECIMAL(5, 2)  NULL,
    diabetes_prevalence   DECIMAL(5, 2)  NULL,
    infant_mortality_rate DECIMAL(5, 2)  NULL,
    adult_male_mortality_rate DECIMAL(6, 3) NULL,
    adult_female_mortality_rate DECIMAL(6, 3) NULL,
    pollution_mortality_rate DECIMAL(5, 2) NULL,
    comorbidity_mortality_rate DECIMAL(5, 2) NULL,
    life_expectancy       DECIMAL(5, 2)  NULL,
    CONSTRAINT PK_Dim_Health PRIMARY KEY (location_key)
);

-- E. Dim_Socioeconomic
CREATE TABLE "Dim_Socioeconomic" (
    location_key          VARCHAR(10)   NOT NULL,
    human_development_index DECIMAL(4, 3) NULL,
    gdp_usd               NUMERIC(19, 2) NULL,
    gdp_per_capita_usd    DECIMAL(15, 2) NULL,
    CONSTRAINT PK_Dim_Socioeconomic PRIMARY KEY (location_key)
);

CREATE TABLE public."Fact" (
    location_key text NOT NULL,
    date date NOT NULL,
    new_confirmed bigint NULL,
    new_deceased bigint NULL,
    cumulative_confirmed bigint NULL,
    cumulative_deceased bigint NULL,
    cumulative_vaccine_doses_administered bigint NULL,
    casos_activos_estimados bigint NULL,
    
    -- Los valores por 1000 deben tener suficiente precisión para > 100
    muertes_por_1000 numeric(10, 3) NULL,
    casos_por_1000 numeric(10, 3) NULL,
    vacunas_por_1000 numeric(10, 3) NULL,
    
    -- Tasas y letalidad
    tasa_letalidad_por_1000 numeric(10, 3) NULL,
    tasa_recuperacion_por_1000 numeric(10, 3) NULL,
    casos_activos_por_1000 numeric(10, 3) NULL,
    letalidad numeric(10, 3) NULL,
    
    CONSTRAINT "Fact_pkey" PRIMARY KEY (location_key, date),
    CONSTRAINT "Fact_location_key_fkey" FOREIGN KEY (location_key) REFERENCES public."Dim_Country"(location_key)
);