from multi_agent_research_system.pipelines.pipeline import run_research_pipeline

def main():
    topic = "Latest advancements in AI research"
    state = run_research_pipeline(topic)
    print(state)

if __name__ == "__main__":
    main()