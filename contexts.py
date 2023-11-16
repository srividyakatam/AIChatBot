def travel_planner_prompt(user_input):
    return f"Act as a Travel Planner with 20 years of experience. You are passionate about nature and exploring different cultures. {user_input}"

def math_teacher_prompt(user_input):
    return f"Act as a Pre-School Math Teacher with 10 years of experience in teaching young children. You make complex concepts easy to understand. {user_input}"

def recipe_generator_prompt(user_input):
    return f"Act as a Recipe Generator AI assistant. You have wide range of knowledge in different cuisiens and you can come up with unexpected recipes.  {user_input}"

def customer_service_agent(user_input):
    return f"Act as a Customer Service Agent who is passionate about helping customers. {user_input}"

def get_contextual_prompt(context, user_input):
    if context == 'travel_planner':
        return travel_planner_prompt(user_input)
    elif context == 'math_teacher':
        return math_teacher_prompt(user_input)
    elif context == 'recipe_generator':
        return recipe_generator_prompt(user_input)
    elif context == 'customer_service_agent':
        return customer_service_agent(user_input)
    else:
        return user_input  # Default case if no context is selected
