from multi_agent_research_system.tools.tools import web_search, scrape_url

def main():
    """query = "Latest advancements in AI research"
    out = web_search(query)   
    print(out)"""
    url = "https://medium.com/@vkt08/seeing-clearly-demystifying-object-detection-performance-metrics-58ac103ae6b3"
    content = scrape_url(url)
    print(content)
if __name__ == "__main__":
    main()