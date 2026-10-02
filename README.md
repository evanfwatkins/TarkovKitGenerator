# TarkovKitGenerator

TarkovKitGenerator is a Python web app built with Dash and hosted with PythonAnywhere. This app acts like a simple toolbelt for Escape from Tarkov players. It provides random loadout generation with optional map selection and is intended to include crafting and upgrade information for Hideout stations. This tool can help a player in game and can also provide some fun raids with the random kit generator. Hideout is temporarily unavailable during this migration.

## Run the application

From the project directory, run:

```powershell
python tarkov_app.py
```

Then open the local URL printed in the terminal (by default, <http://127.0.0.1:8050>).

## Data source migration

The kit generator uses the Tarkov.dev public JSON API locally and a bundled snapshot on PythonAnywhere, where outbound API access is unavailable:

- Item data: <https://json.tarkov.dev/pve/items>
- Endpoint list and supported datasets: <https://json.tarkov.dev/endpoints>

By default, local runs load item data from the JSON API. On a successful API refresh, the compact generator dataset is saved to `data/pve-items.json` in the project and to a 24-hour cache under the user's home directory. The project snapshot can then be deployed to PythonAnywhere with the application. If a local API refresh fails, the loader uses the last cached dataset or the project snapshot.

Set `TARKOV_DATA_SOURCE=bundled` in the PythonAnywhere WSGI file before importing `tarkov_app` to make the hosted app load only the bundled file and never attempt outbound requests:

```python
import os
os.environ["TARKOV_DATA_SOURCE"] = "bundled"

from tarkov_app import server as application
```

For local API access, omit the setting or set `TARKOV_DATA_SOURCE=api`. The kit generator loads data once into an in-memory store and reuses it for each generated kit. Item `types`, `inspectImageLink`, `blocksHeadphones`, and `normalizedName` fields drive item selection and compatibility. When the JSON API returns a placeholder `name`, the app uses the item Wiki link as a readable-name fallback.

### Migration track

- [x] Use the JSON item endpoint and map its item fields into the kit generator.
- [x] Simplify gear filtering to item types and blocking metadata instead of hard-coded item-name lists.
- [x] Add a collapsible footer panel showing the final generated items as JSON.
- [x] Mark Hideout unavailable while kit generation is migrated.
- [ ] Confirm the JSON API's translated item-name behavior and improve the fallback if needed.
- [ ] Migrate and re-enable Hideout upgrades and crafts after validating the kit generator.

### Data-store and performance trade-offs

The current in-memory data store is intentionally simple: each kit uses local random selection, so generation does not wait for API requests. Its trade-offs are that data is fixed for the life of the process, each app worker has its own copy, and the first run after the cache expires must download and parse the full item dataset. The compact disk cache reduces repeat startup downloads and supports stale-data fallback, at the cost of data being up to 24 hours old.

Possible future improvements:

- Use a shared cache such as Redis only if multiple workers or instances make duplicated memory and cache refreshes a measurable problem; it adds an external service to operate.
- Pre-fetch and refresh the compact cache on a schedule to avoid making first-startup latency depend on the API.
- Kit images use native lazy loading; consider smaller image variants and explicit image dimensions to reduce transfer and layout shift.
- If image requests remain slow, proxy/cache the Tarkov image CDN locally or through a CDN near the app. This adds storage and cache-invalidation work, so measure browser network timings first.

## Resources

- Tarkov API source project: <https://github.com/the-hideout/tarkov-api>
- Tarkov.dev JSON API: <https://json.tarkov.dev/endpoints>
- Tarkov.dev: <https://tarkov.dev/>
