# ⚽ Match Metrics Index (MMI)

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Tests](https://img.shields.io/badge/Tests-101%20Passing-brightgreen)
![GitHub release](https://img.shields.io/github/v/release/StylianosOrfanou/match-metrics-index)
![License](https://img.shields.io/github/license/StylianosOrfanou/match-metrics-index)

## Overview

MMI (Match Metrics Index) is a football prediction engine that transforms raw football data into dynamic team ratings and probabilistic match predictions using statistical modelling and Monte Carlo simulation.

The project combines **season statistics**, **recent team form**, **dynamic rating generation**, **Poisson probability modelling**, and **Monte Carlo simulation** to generate accurate football match predictions.

All team ratings are generated automatically from the Sportmonks Football API, allowing the model to update itself throughout the season without manual intervention.

---

# Features

- Dynamic team rating generation
- Automatic Sportmonks API integration
- Season statistics engine
- Recent form engine (Last 5 Matches)
- Rating Fusion Engine
- Expected Goals (xG) calculation
- Poisson probability model
- Monte Carlo simulation
- Match outcome probabilities (1X2)
- Goals markets (GG / Over / Under)
- Correct score probabilities
- Validation framework
- One-command database update
- Automatic JSON generation
- Automatic database backups

---

# Architecture

```
Sportmonks API
        │
        ▼
Season Statistics Repository
        │
        ▼
Rating Builder
        │
        ▼
Season Ratings
        │
        ├───────────────┐
        ▼               │
Recent Form Repository  │
        ▼               │
Recent Rating Builder   │
        ▼               │
Recent Ratings          │
        └──────┬────────┘
               ▼
      Rating Fusion Engine
               ▼
     Rating Pipeline Service
               ▼
         Prediction Engine
               ▼
      Monte Carlo Engine
               ▼
          Match Prediction
```

---

# Project Structure

```
clients/
config/
data/
engines/
exporters/
models/
presentation/
repositories/
scripts/
services/
tests/
validation/
```

---

# Example Prediction

```
----------------------------------------
MMI MATCH PREDICTION
----------------------------------------

Pafos FC Overall Rating: 75.90
Omonia Overall Rating: 95.00

Pafos FC xG: 1.35
Omonia xG: 1.74

Home Win : 29.88%
Draw     : 23.42%
Away Win : 46.70%

Most Likely Score
1-1 (10.69%)

Monte Carlo (10,000 Simulations)

Home Win : 30.62%
Draw     : 22.97%
Away Win : 46.41%
```

---

# Data Sources

- Sportmonks Football API
- League statistics
- Team season statistics
- Recent match form

---

# Database Update

Update the entire database with a single command:

```bash
python -m scripts.update_database
```

This command automatically:

- Downloads the latest season statistics
- Downloads the latest recent form
- Calculates season ratings
- Calculates recent ratings
- Fuses both rating models
- Generates `teams.json`
- Creates automatic backups

---

# Testing

The project currently contains **101 automated tests**.

Run all tests:

```bash
python -m pytest
```

---

# Current Version

## ✅ Version 1.0

Implemented:

- Dynamic Rating Engine
- Recent Form Engine
- Rating Fusion
- Prediction Engine
- Expected Goals Model
- Poisson Distribution
- Monte Carlo Simulation
- Validation Framework
- Automatic Team Builder
- Automatic Database Update
- Automatic Backups

---

# Roadmap

## Version 1.1
- Elo Rating Engine

## Version 1.2
- Probability Calibration
- Market Calibration

## Version 1.3
- Value Betting Engine

## Version 1.4
- Injuries & Suspensions

## Version 1.5
- Rest Days
- Travel Fatigue

## Version 2.0
- Multi-League Support
- REST API
- Web Dashboard
- Live Predictions

---

# Tech Stack

- Python 3.13
- Sportmonks Football API
- Pytest
- Monte Carlo Simulation
- Poisson Distribution
- JSON Data Pipeline
- Repository Pattern
- Service Layer Architecture

---

# Author

**Stylianos Orfanou**

Football Analytics • Python Development • Sports Data Science

GitHub: https://github.com/StylianosOrfanou 