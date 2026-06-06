# Autobrowse Proof

Autobrowse proof captures browser or HTTP evidence for UI and runtime behavior.

Source-code proof and live runtime proof are different. A passing test can prove source behavior. A browser screenshot, HTTP response, or normalized runtime artifact can prove what a running app exposed at a point in time.

## Acceptable Proof

- Sanitized HTTP status and response summary
- Screenshot path without private data
- Browser console summary
- Accessibility snapshot summary
- Normalized runtime artifact copied through a safe bridge

## Receipt Link

Autobrowse proof should be attached to a completion receipt and a trace event. The receipt should say whether the proof came from source validation, live runtime validation, or both.

## Safety

Do not store raw private pages, secrets, tokens, credentials, customer data, or unrestricted runtime logs in public proof artifacts.
