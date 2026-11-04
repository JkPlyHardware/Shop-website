# Test report

## Checks performed while preparing this source package

- Python `compileall` over the backend source: **passed** (syntax compilation only).
- Project ZIP archive creation and file presence: **passed**.
- `node --check` for the plain-JavaScript API helper and Vite config: **passed**.

## Not executed in this environment

- `python manage.py check` and `python manage.py test`: **not run** because Django/DRF and other Python dependencies could not be installed in this offline build environment.
- `npm run lint` and `npm run build`: **not run** because frontend dependencies were not installed (npm registry access unavailable).
- Browser/device testing at 320, 375, 425, 768, 1024 and 1440 px: **not run**.

Run the commands in the root `README.md` on your computer after installing dependencies. Do not treat a syntax compilation check as a substitute for Django's system checks or frontend build.
