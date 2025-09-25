import streamlit as st
import random

# --- Step 1: Mock Data and Retrieval Function (Simulating the RAG 'Retrieval' part) ---
# This is our mock internal knowledge base. In a real-world scenario, this would be a vector database
# containing information from policy documents, FAQs, and customer data.

MOCK_POLICY_DATA = {
    "policy_1001": {
        "customer_name": "Jane Doe",
        "policy_type": "Auto Insurance",
        "coverage": {
            "collision": "Up to $50,000",
            "comprehensive": "Up to $25,000",
            "roadside_assistance": "Included",
        },
        "premium": "$120/month",
        "deductible": "$500",
        "exclusions": "Off-road driving and commercial use.",
    },
    "policy_1002": {
        "customer_name": "John Smith",
        "policy_type": "Home Insurance",
        "coverage": {
            "fire": "Full replacement value",
            "theft": "Up to $10,000",
            "natural_disaster": "Not included (separate policy)",
        },
        "premium": "$85/month",
        "deductible": "$1,000",
        "exclusions": "Damage from floods and earthquakes.",
    },
}

def retrieve_policy_info(query):
    """
    Simulates retrieving relevant policy information based on a query.
    In a real system, this would involve semantic search or keyword matching
    against a large knowledge base. For this MVP, we'll use simple keyword matching.
    """
    retrieved_info = []
    
    # Simple keyword-based retrieval logic
    for policy_id, policy_details in MOCK_POLICY_DATA.items():
        if policy_id in query or policy_details["customer_name"].lower() in query.lower():
            retrieved_info.append(policy_details)
            
    return retrieved_info

# --- Step 2: The Generative AI Logic (Simulating the 'Generation' part) ---
# This function acts as our simple LLM. It takes the retrieved information
# and the user's query to generate a context-aware response.
def generate_response(query, context):
    """
    Generates a response using the provided context.
    For this MVP, it's a simple template-based response, but it demonstrates
    the core concept of using retrieved data to inform the output.
    """
    if not context:
        return "I'm sorry, I couldn't find any relevant policy information for that query. Please check the policy number or customer name."
    
    # Assume we're focusing on one customer for this simplified MVP
    policy = context[0]
    customer_name = policy["customer_name"]
    policy_id = [k for k, v in MOCK_POLICY_DATA.items() if v == policy][0]

    # Generate a context-specific response
    if "coverage" in query.lower():
        coverage_list = [f"- {key.replace('_', ' ').title()}: {value}" for key, value in policy["coverage"].items()]
        coverage_text = "\n".join(coverage_list)
        return f"Hello, the policy details for {customer_name} (Policy ID: {policy_id}) indicate the following coverage:\n\n{coverage_text}"
        
    elif "premium" in query.lower():
        return f"The monthly premium for {customer_name}'s policy (Policy ID: {policy_id}) is {policy['premium']}."
        
    elif "deductible" in query.lower():
        return f"The deductible for {customer_name}'s policy (Policy ID: {policy_id}) is {policy['deductible']}."
        
    else:
        # A simple fallback for other queries
        return f"Based on the information for {customer_name} (Policy ID: {policy_id}), I can confirm that the policy type is '{policy['policy_type']}'. How can I assist further?"

# --- Step 3: Streamlit UI Development ---

st.title("🤖 Gen AI-Powered CSR Assistant")
st.markdown("Enter a customer's policy number or name and their query to get a quick response.")
st.markdown("---")

# Main chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter customer's query (e.g., 'What is the coverage for Jane Doe?'):"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simulate the AI assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Step A: Retrieve information
            context = retrieve_policy_info(prompt)
            # Step B: Generate response using context
            response = generate_response(prompt, context)
            
            # Display the generated response
            st.markdown(response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
