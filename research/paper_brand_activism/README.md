# Paper: Brand Activism and Consumer Response

## Research Question
Does brand activism on social media affect consumer sentiment, and does the effect
vary by brand-cause congruence?

## Data
- **Source:** Twitter/X API v2 — academic research track
- **Period:** 2021-01-01 to 2023-12-31
- **Version:** raw data downloaded 2024-03-10, stored in `/data/raw/`
- **Size:** ~420,000 brand posts, ~2.1M consumer replies

## Identification Strategy
Difference-in-differences using brand activism events as treatment.
Key assumption: parallel trends in sentiment pre-event.
Robustness: placebo events, alternative pre-periods.

## Reproducing Results

```bash
# 1. Install dependencies
pip install -r ../../../../requirements.txt

# 2. Preprocess raw data
python src/preprocessing/clean_tweets.py

# 3. Run sentiment classification
python src/models/sentiment_classifier.py

# 4. Estimate DiD model
python src/analysis/did_estimation.py

# 5. Generate all tables and figures
python src/analysis/tables_figures.py
# Outputs saved to: outputs/figures/ and outputs/tables/
```

## Journal Target
Journal of Marketing Research (A*)

## Notes
- Main result: Table 3, Column 4
- Heterogeneity by congruence: Table 5
- Robustness checks: Appendix B
