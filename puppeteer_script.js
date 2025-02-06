import puppeteer from 'puppeteer';

async function searchGoogle(query) {
    console.log(JSON.stringify({ status: "starting", query }));
    
    const browser = await puppeteer.launch({ 
        headless: false,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        console.log(JSON.stringify({ status: "navigating" }));
        await page.goto('https://www.google.com', {
            waitUntil: 'networkidle2'
        });
        
        console.log(JSON.stringify({ status: "typing" }));
        await page.waitForSelector('textarea[name="q"]', { visible: true });
        await page.click('textarea[name="q"]');
        await page.type('textarea[name="q"]', query);
        
        console.log(JSON.stringify({ status: "searching" }));
        await Promise.all([
            page.waitForNavigation({ waitUntil: 'networkidle2' }),
            page.click('input[type="submit"]')
        ]);
        
        console.log(JSON.stringify({ status: "extracting" }));
        await page.waitForSelector('.g');
        
        const results = await page.evaluate(() => {
            const titles = Array.from(document.querySelectorAll('.g h3'));
            return titles.slice(0, 10).map(title => title.textContent);
        });
        
        console.log(JSON.stringify(results));
        return results;
        
    } catch (error) {
        console.log(JSON.stringify({ error: error.message }));
    } finally {
        await browser.close();
    }
}

// Get the search query from command line arguments
const searchQuery = process.argv[2] || 'top restaurants near me';
searchGoogle(searchQuery);