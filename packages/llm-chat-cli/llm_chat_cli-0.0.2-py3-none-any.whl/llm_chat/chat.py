"""
Core chat functionality for interacting with LLM providers
"""

def chat_with_ai(client, provider, model, messages):
    """
    Handle chat interactions with different AI providers.
    
    Args:
        client: The initialized client instance for the provider
        provider (str): The name of the provider ('groq', 'openai', etc.)
        model (str): The model name to use
        messages (list): List of message dictionaries containing the conversation history
    
    Returns:
        str: The AI's response text, or None if an error occurs
    """
    try:
        if provider == 'groq':
            response = client.chat.completions.create(
                messages=messages,
                model=model,
            )
            return response.choices[0].message.content
            
        elif provider == 'openai':
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content
            
        elif provider == 'anthropic':
            response = client.messages.create(
                model=model,
                messages=messages,
                max_tokens=4096,
                stream=False
            )
            return response.content[0].text
            
        elif provider == 'cerebras':
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
            
    except Exception as e:
        print(f"Error occurred while communicating with {provider}: {str(e)}")
        return None