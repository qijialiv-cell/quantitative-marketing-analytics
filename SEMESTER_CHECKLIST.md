# Semester Maintenance Checklist

## Start of Semester

- [ ] Create new dated folder: `teaching/YYYY_term/`
- [ ] Copy and update slides from previous semester (do not overwrite originals)
- [ ] Update module README files with current term and cohort info
- [ ] Pin dependency versions: update `requirements.txt`
- [ ] Run all lab notebooks end-to-end (`jupyter nbconvert --to notebook --execute`)
- [ ] Verify all Streamlit apps load (`streamlit run app.py`)
- [ ] Confirm deployed URLs are live and up-to-date
- [ ] Update `quarto/website/index.qmd` with current term's module links
- [ ] Re-render and redeploy Quarto site (push to `main`)

## End of Semester

- [ ] Commit final versions of all slides and lab notebooks
- [ ] Strip notebook outputs before commit (`nbstripout --install` / `git add`)
- [ ] Archive any apps no longer actively deployed (note in README)
- [ ] Document known issues and improvements in module README
- [ ] Tag the repo with the semester: `git tag 2026-spring`

## Each Paper Milestone

- [ ] Ensure full reproduction pipeline is documented in paper `README.md`
- [ ] Raw data is untouched in `/data/raw/`
- [ ] All outputs can be regenerated from scratch
- [ ] Robustness checks committed alongside main results
