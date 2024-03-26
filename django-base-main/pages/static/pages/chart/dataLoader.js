export function setupButtons() {
    // Helper functions
    const get = async (url) => {
        const response = await fetch(url, {
            method: "GET"
        });

        return await response.json();
    }

    const updateStatus = (status) => {
        document.getElementById('app-xhr-status').innerHTML = status;
    }

    // Calls server endpoint instructing it to load events from pages/data/solar_events.json
    const loadSolarEvents = () => {
        get("/pages/load_solar_events")
            .then((response) => {
                if (response.result != "ok") {
                    updateStatus("Failed to load solar events from disk")
                    return
                }
                updateStatus("Loaded solar events from disk")
                window.location.reload();
            })
    }

    // Calls server endpoint instructing it to call Wikipedia's API for article revisions, persisting them to the backend DB
    const getArticleRevisions = () => {
        updateStatus("Querying Wikipedia API - ETA ~1 minute...")
        // Disable button after click
        document.querySelector('#app-pull-revisions').setAttribute("disabled", "");

        get("/pages/scrape_revisions")
            .then((response) => {
                if (response.result != "ok") {
                    updateStatus("Failed to read Wikipedia API/persist to DB or data already exists/scrape in progress: " + response.result)
                    document.querySelector('#app-pull-revisions').removeAttribute("disabled");
                    return
                }
                updateStatus("Success: pulled revision data from Wikipedia articles")
                window.location.reload();
            })
    }

    // Event listeners
    document
        .querySelector('#app-load-solar-events')
        .addEventListener('click', loadSolarEvents);
    
    document
        .querySelector('#app-pull-revisions')
        .addEventListener('click', getArticleRevisions);
}