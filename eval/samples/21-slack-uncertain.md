---
type: slack
facts:
  - the deploy might slip to Thursday
  - writer thinks the migration is the blocker but is not sure yet
  - about 3 of 40 integration tests are failing
  - writer will post an update by 4pm
may_drop:
  - "100"
keep:
  - "might|may|could|possibly|probably"
  - "Thursday"
  - "not sure|unsure|not certain|I think|probably|my guess|looks like"
  - "\\b3\\b|three"
  - "\\b40\\b|forty"
  - "4\\s?pm|4:00"
forbid:
  - "\\bwill (?:slip|be delayed|move)"
  - "\\bmost (?:of the )?tests\\b|\\bmany tests\\b"
  - "\\bthe migration is (?:definitely )?(?:the|what'?s) (?:blocker|blocking)\\b(?![^.]*(?:think|sure|guess))"
---
Hey team! 👋 Quick update on the deploy: it's looking like it might slip to Thursday. I think the migration is the main blocker here, but I'm not 100% sure yet — still digging in. Currently, about 3 of our 40 integration tests are failing. I'll circle back with a comprehensive update by 4pm. Thanks so much for your patience and understanding! 🙏
