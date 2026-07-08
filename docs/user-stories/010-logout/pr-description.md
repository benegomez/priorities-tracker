# PR #10 — US-010: Logout — Cerrar Sesión

## Summary

Adds a visible logout button to the application Header. Users can now click their avatar to open a dropdown menu with "Cerrar sesión" option. The backend endpoint and frontend logic already existed (US-002) — this PR connects them to the UI.

## Type of Change

- [x] New feature (non-breaking)
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation only

## Risk Level

**Low** — Frontend-only. No new endpoints. Connects existing `useLogout()` hook to a new UI button.

## What Changed

### New Files (2)
| File | Purpose |
|---|---|
| `components/layout/UserMenu.tsx` | Dropdown menu with avatar trigger + "Cerrar sesión" |
| `src/tests/user-menu.test.tsx` | 3 component tests |

### Modified Files (1)
| File | Change |
|---|---|
| `components/layout/Header.tsx` | Replaced static user info block with `<UserMenu />` |

## Key Design Decisions

1. **Simple dropdown** — Used a custom dropdown with `useRef` + click-outside listener instead of installing a new shadcn component. Keeps bundle small.

2. **Fail-safe logout** — `useLogout` hook uses `onSettled` (not `onSuccess`), so cookies and store are always cleared even if the API call fails.

3. **Accessibility** — Full ARIA support: `aria-expanded`, `aria-haspopup="menu"`, `role="menu"`, `role="menuitem"`, Escape key closes dropdown.

## Pre-existing Code Reused

| Artefact | Origin |
|---|---|
| `POST /api/v1/auth/logout` | US-002 |
| `useLogout()` hook | US-002 |
| `logout()` service | US-002 |
| `clearUser()` store | US-002 |

## Testing Evidence

- **Component tests:** 3 new tests, all passing
- **Total tests:** 58/58 ✅
- **Build:** `npx next build --no-lint` successful
- **Existing Header tests:** still passing (renders user name + hamburger)

## Screenshots / Verification

Header now shows clickable avatar → dropdown with "Cerrar sesión":
- Click → dropdown opens
- "Cerrar sesión" → API call + cookie cleanup + redirect to /auth/login
- Loading state: "Cerrando..." + disabled button
- Click outside or Escape → dropdown closes
