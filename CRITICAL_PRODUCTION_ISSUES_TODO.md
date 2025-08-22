# CRITICAL PRODUCTION ISSUES TODO LIST

## Issues to Fix:

```markdown
- [ ] 1. Sentiment analysis 500 error for specific symbols (e.g., DNB.OL)
- [ ] 2. Stocks compare page 500 error  
- [ ] 3. Market status in premium banner - verify real data usage
- [ ] 4. Stock details pages issues:
  - [x] 4a. Portfolio button stuck on "Legger til" (Adding) indefinitely - FIXED: parameter mapping
  - [x] 4b. Volume and Market cap showing "-" instead of real data - FIXED: added missing fields
  - [ ] 4c. Chart sections showing "Henter kursdata..." (Loading chart data) indefinitely
  - [ ] 4d. Key metrics showing "-" for all values under "Nøkkeltall"
  - [ ] 4e. Fundamental tab showing "-" for all fields
  - [ ] 4f. Company info tab showing "Ikke tilgjengelig" (Not available)
  - [ ] 4g. Technical analysis RSI and MACD boxes are empty
- [ ] 5. Recommendations routing issues:
  - [ ] 5a. "Se fullstendig anbefaling" button links to general recommendations instead of ticker-specific
  - [ ] 5b. AI analysis page recommendation button has same routing issue
- [ ] 6. Technical analysis search field stopped working
```

## Priority Order:
1. ~~Portfolio button fix (critical user interaction)~~ ✅ COMPLETED
2. ~~Data display fixes (volume, market cap, metrics)~~ ✅ COMPLETED
3. Chart loading issues
4. Recommendation routing fixes
5. Search functionality restore
6. Sentiment analysis error
7. Stocks compare error
