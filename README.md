# TarkovKitGenerator

TarkovKitGenerator is a Python web app built with Dash and hosted with PythonAnywhere. It provides random loadout generation, map selection, and Hideout information.

## Run the application

From the project directory, run:

```powershell
python tarkov_app.py
```

Then open the local URL printed in the terminal (by default, <http://127.0.0.1:8050>).

## Data source migration

The app is moving from the unavailable Tarkov.dev GraphQL endpoint to the public JSON API:

- Item data: <https://json.tarkov.dev/pve/items>
- Endpoint list and supported datasets: <https://json.tarkov.dev/endpoints>

The kit generator loads item data once into an in-memory data store and reuses it for each generated kit. A compact local cache under the user's home directory is refreshed every 24 hours and used as a fallback if the API is unavailable. Item `types`, `inspectImageLink`, `blocksHeadphones`, and `normalizedName` fields drive item selection and compatibility. The JSON API currently returns placeholder `name` values for some records, so the app uses the item Wiki link as a readable-name fallback.

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
