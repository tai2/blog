const process = require('process')
const path = require('path')
const fs = require('fs')
const puppeteer = require('puppeteer')
const restructured = require('restructured').default

function parseArticle(path) {
    const text = fs.readFileSync(path, 'utf8')
    const article = restructured.parse(text)
    const firstSection = article.children.find(child => child.type === 'section')
    const firstTitle = firstSection.children.find(child => child.type === 'title')
    const firstTitleText = firstTitle.children.find(child => child.type === 'text')
    return {
        path,
        title: firstTitleText.value,
    }
}

async function capture(article) {
    const viewport = {
        width: 1000,
        height: 500,
    }
    const injectedProps = {
        title: article.title,
    }
    const basename = path.basename(article.path, '.rst')

    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    page.setViewport(viewport)
    await page.exposeFunction('getInjectedProps', () => injectedProps)
    await page.goto('file://' + path.resolve('ogimage.html'))
    await page.screenshot({path: `content/images/og/${basename}.png`})
    await browser.close()
}

const article = parseArticle(process.argv[2])
capture(article)
