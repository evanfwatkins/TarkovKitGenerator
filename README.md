Tarkov API https://github.com/the-hideout/tarkov-api -->
Log into CloudFlare and make sure the environment is deployed
https://dash.cloudflare.com/acfd88b04d4aa267f5bb9b94ee3451e2/workers/services/view/tarkovkitgeneratorcloudfare/production/metrics

1) Run "wrangler login" - (needed for k/v store and secrets)
2) Start the dev environment by running "npm run dev"



TO DO: 
    get app.py to call the kit_builder function
    Resolve the UI in DASH to have only one input but 6 outputs and a text output
    parse the response into something visual
    display the icon in the output of each gear slot