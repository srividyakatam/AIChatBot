# Professional: Formal, business-like responses.
def professional_style(user_input):
    return f"You have Professional personality style with formal, business-like responses. {user_input}"

# Friendly: Casual, warm, and conversational.
def friendly_style(user_input):
    return f"You have Friendly personality style with casual, warm and conversational responses. {user_input}"

# Humorous: Light-hearted, often includes jokes or witty remarks.
def humorous_style(user_input):
    return f"You have Humorous personality style with light-hearted responses include jokes and witty remarks as appropriate. {user_input}"

# Empathetic: Understanding, supportive, and reassuring.
def empathetic_style(user_input):
    return f"You have Empathetic personality with understanding, supportive and reassuring responses. {user_input}"

def get_personality_style(personality, user_input):
    if personality == 'professional':
        return professional_style(user_input)
    elif personality == 'friendly':
        return friendly_style(user_input)
    elif personality == 'humorous':
        return humorous_style(user_input)
    elif personality == 'empathetic':
        return empathetic_style(user_input)
    else:
        return user_input  # Default case if no personality is selected


# For each personality, create templates or guidelines for responses. This can include:
# Language Style: Choice of words, sentence structure, and level of formality.
# Emotional Tone: Level of enthusiasm, empathy, or humor.
# Response Strategy: How the bot addresses questions or concerns.