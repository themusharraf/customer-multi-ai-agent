from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool

# 🔑 Serper (Google Search) uchun
search_tool = SerperDevTool()

# 🌐 Web sahifani skreyp qilish uchun
scrape_tool = ScrapeWebsiteTool()

docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://docs.crewai.com"
)

# 🔎 To‘liq veb saytlarda qidirish uchun
website_search = WebsiteSearchTool()

# Endi ularni CrewAI agentga ulash mumkin

