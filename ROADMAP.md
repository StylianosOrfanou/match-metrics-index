# MMI – Mezes Match Index

## Model Type
Hybrid football prediction model combining statistical data with contextual football factors.

## Team Ratings
- Attack Rating
- Defence Rating
- Form Rating
- Home Rating
- Away Rating

## Match Factors
- Home Advantage
- Rest Days
- Injuries and Suspensions
- Expected Line-up
- European Fatigue
- Rotation
- Coaching Changes
- Match Fitness
- Squad Quality
- Tactical Match-up
- Motivation
- Head-to-Head

## Prediction Pipeline
Team Ratings
→ Match Factors
→ Expected Goals
→ Poisson Model
→ Monte Carlo Simulation
→ MMI Probabilities
→ Confidence Score
→ Biggest Factors

## Development Roadmap

### Phase 1
- [x] Project setup
- [x] API connection
- [x] Team search
- [x] Basic Form Rating
- [ ] Form Rating v2
- [ ] Attack Rating
- [ ] Defence Rating
- [ ] Expected Goals
- [ ] Poisson Model
- [ ] Monte Carlo Simulation

### Phase 2
- [ ] Home and Away Ratings
- [ ] Rest Days
- [ ] Injuries and Suspensions
- [ ] European Fatigue
- [ ] Rotation
- [ ] Squad Quality
- [ ] Confidence Rating

### Phase 3
- [ ] Tactical Match-up
- [ ] Automated explanation
- [ ] Historical validation
- [ ] Instagram output
- [ ] MMI v1.0