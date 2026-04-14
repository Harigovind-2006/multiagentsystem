from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain, reviewer_chain

def run_research_pipeline(topic: str) -> dict:
    
    state ={}
    
    #search agent working
    print("\n" + "="*50)
    print("Phase 1: Searching the Web...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "message": [("user", f"Find the latest and most reliable information on: {topic}")]

    })
    
    state["search_result"] = search_result["message"][-1].content
    print("\n search result:")
    print(state["search_result"])
    

    #reader agent working
    print("\n" + "="*50)
    print("Phase 2: Reading and Extracting Information...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "message": [("user", 
            f"Based on the following search results about {topic}"
            f"pick the most relevant urls and scrape it for deeper contend.\n\n"
            f"Search results:\n{state['search_result'][:800]}"
        )]
    })
    
    state["scraped_content"] = reader_result["message"][-1].content
    print("\n Scraped Content:")
    print(state["scraped_content"])

    #writer chain working
    print("\n" + "="*50)
    print("Phase 3: Writing the Report...")
    print("="*50)

    research_combined = (

        f"Search Results:\n{state['search_result']}\n\n"
        f"Scraped Content:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    
    print("\n Research Report:")
    print(state["report"])

    #critic chain working
    print("\n" + "="*50)
    print("Phase 4: Critiquing the Report...")
    print("="*50)

    state["critic_feedback"] = critic_chain.invoke({
        "report": state["report"]
    })
    print("\n Critic Feedback:")
    print(state["critic_feedback"])

    #reviewer chain working
    print("\n" + "="*50)
    print("Phase 5: Reviewing and Improving the Report...")
    print("="*50)

    state["final_report"] = reviewer_chain.invoke({
        "report": state["report"],
        "feedback": state["critic_feedback"]
    })
    print("\n Final Report:")
    print(state["final_report"])

    return state

if __name__ == "__main__":
    topic = input("Enter the topic you want research on: ")
    result = run_research_pipeline(topic)
    print("\n" + "="*50)
    print("Research Pipeline Completed!")
    print("="*50)
    print("\n Final Report:")
    print(result["final_report"])


    

    

