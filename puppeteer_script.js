import puppeteer from 'puppeteer';

async function executeTask(subtask) {
    console.log(JSON.stringify({ status: "starting", subtask }));
    
    const browser = await puppeteer.launch({
        headless: false,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();
        
        // Navigate to starting URL if provided
        if (subtask.url) {
            await page.goto(subtask.url, { waitUntil: 'networkidle2' });
        }
        
        // Execute the specific action
        switch (subtask.action) {
            case 'search_google':
                await searchGoogle(page, subtask.query);
                break;
            case 'navigate_imdb':
                await navigateToIMDB(page);
                break;
            case 'extract_movies':
                return await extractTopMovies(page, subtask.count);
            case 'get_actor_info':
                return await getActorInfo(page, subtask.actor_name);
            // Add more actions as needed
        }
        
        // Extract requested data if specified
        if (subtask.data_to_extract) {
            const data = await extractData(page, subtask.data_to_extract, subtask.selectors);
            return { [subtask.action]: data };
        }
        
    } catch (error) {
        console.error(JSON.stringify({ error: error.message }));
        throw error;
    } finally {
        await browser.close();
    }
}

// Helper functions for specific actions
async function searchGoogle(page, query) {
    await page.waitForSelector('textarea[name="q"]');
    await page.type('textarea[name="q"]', query);
    await Promise.all([
        page.waitForNavigation(),
        page.keyboard.press('Enter')
    ]);
}

async function extractData(page, dataType, selectors) {
    await page.waitForSelector(selectors[dataType]);
    return await page.evaluate((selector) => {
        const elements = document.querySelectorAll(selector);
        return Array.from(elements).map(el => el.textContent);
    }, selectors[dataType]);
}

// Parse command line argument and execute
const subtask = JSON.parse(process.argv[2]);
executeTask(subtask)
    .then(result => console.log(JSON.stringify(result)))
    .catch(error => console.error(JSON.stringify({ error: error.message })));