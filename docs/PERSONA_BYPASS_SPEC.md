# Persona Bypass for Automated Testing

## Summary

Add a bypass for Persona identity verification in DEV environment for test accounts using the `@testinator.email` domain. This enables automated E2E testing without requiring camera/biometric interaction.

## Problem

Persona's liveness detection requires:
- Camera access for selfie capture
- Real-time face movement detection
- Biometric matching against ID document

This is **by design** anti-automation. Even in Sandbox mode with "Pass verifications" enabled, the UI flow still requires camera access which automated tests cannot provide.

## Solution

**Bypass Persona for test email domains in DEV environment only.**

### Implementation

```javascript
// Pseudocode - add to signup/onboarding flow

const TEST_EMAIL_DOMAINS = [
  'testinator.email',
  'team887961.testinator.email'
];

const isTestAccount = (email) => {
  const domain = email.split('@')[1];
  return TEST_EMAIL_DOMAINS.some(testDomain =>
    domain === testDomain || domain.endsWith('.' + testDomain)
  );
};

// In the onboarding flow where Persona is triggered:
if (process.env.NODE_ENV === 'development' && isTestAccount(user.email)) {
  // Skip Persona verification
  // Mark user as verified (or set a test verification flag)
  await markUserAsVerified(user.id, { bypassReason: 'test_account' });
  redirectToNextStep();
} else {
  // Normal Persona flow
  launchPersonaInquiry();
}
```

### Conditions for Bypass

| Condition | Required |
|-----------|----------|
| Environment is DEV (`app-dev.thelicenseauthority.com`) | Yes |
| Email domain matches test pattern (`*@*.testinator.email`) | Yes |
| Production environment | **Never bypass** |
| Staging environment | Optional (discuss) |

### Test Email Pattern

```
*@team887961.testinator.email
```

Examples:
- `roger.dev.test.001@team887961.testinator.email`
- `e2e.dunkin.001@team887961.testinator.email`
- `automated.circlek@team887961.testinator.email`

## Security Considerations

1. **DEV only** - Never enable in production
2. **Specific domain** - Only `testinator.email` (our Mailinator private domain)
3. **Audit logging** - Log when bypass is used for traceability
4. **Environment check** - Double-check environment before bypassing

## Testing Flow After Implementation

```
1. Navigate to app-dev.thelicenseauthority.com
2. Sign up with test@team887961.testinator.email
3. Complete Auth0 signup (email + password + TOTP)
4. Verify email via Mailinator API
5. **Persona step is SKIPPED** (bypass triggers)
6. Land directly on onboarding/dashboard
7. Continue with company setup, address entry, etc.
```

## What We're Testing vs. Not Testing

### We ARE testing:
- Auth0 signup/login flow
- TOTP enrollment and verification
- Email verification via Mailinator
- Company profile creation
- Address entry and geocoding
- License discovery
- Team invitations
- All application functionality

### We are NOT testing:
- Persona ID verification (tested separately by Persona/manually)
- Biometric liveness detection
- Document OCR accuracy

This is appropriate because Persona is a third-party service with its own QA. Our E2E tests focus on **our application's functionality**.

## Acceptance Criteria

- [ ] Test accounts with `@testinator.email` skip Persona in DEV
- [ ] Normal accounts still go through Persona in DEV
- [ ] All environments except DEV require Persona for all accounts
- [ ] Bypass is logged for audit purposes
- [ ] No changes to production behavior

## Priority

**HIGH** - Blocking automated E2E testing capability

## Requested By

Automated Testing Team - Roger

## Date

2025-12-21
