# /home/ubuntu/neonadsai_backend/src/ai_services/content_generator.py

import os
import random

# Simple placeholder for OpenAI functionality
# This is a pure Python implementation with no native dependencies

def generate_ad_copy(prompt, model=None, max_tokens=None, num_variations=3):
    """Generates ad copy variations based on a given prompt using a simple template system.
    This is a placeholder that doesn't require OpenAI or any native dependencies."""
    
    print("Using pure Python content generator (no OpenAI).")
    
    # Extract key information from prompt if available
    product = "your product"
    audience = "customers"
    benefits = ["benefit"]
    
    # Try to parse the prompt for better templates
    if "Product:" in prompt:
        try:
            product_part = prompt.split("Product:")[1].split(".")[0].strip()
            product = product_part
        except:
            pass
            
    if "Target Audience:" in prompt:
        try:
            audience_part = prompt.split("Target Audience:")[1].split(".")[0].strip()
            audience = audience_part
        except:
            pass
            
    if "Key Selling Points:" in prompt or "Benefits:" in prompt:
        try:
            if "Key Selling Points:" in prompt:
                benefits_part = prompt.split("Key Selling Points:")[1].split(".")[0].strip()
            else:
                benefits_part = prompt.split("Benefits:")[1].split(".")[0].strip()
                
            benefits = [b.strip() for b in benefits_part.split(",")]
        except:
            pass

    # Template headlines
    headlines = [
        f"Discover the Perfect {product}",
        f"{product} - Made for {audience}",
        f"Elevate Your Experience with {product}",
        f"The {product} You've Been Waiting For",
        f"Why {audience} Choose Our {product}",
        f"Introducing: The Ultimate {product}",
        f"Transform Your Life with {product}",
        f"The Smart Choice: {product}",
        f"{product} - Quality You Can Trust",
        f"Experience the {product} Difference"
    ]
    
    # Template body texts
    body_templates = [
        f"Designed specifically for {audience}. {random.choice(benefits).capitalize()} and more. Try it today!",
        f"Join thousands of satisfied {audience} who love our {product}. {random.choice(benefits).capitalize()}!",
        f"Our {product} offers {random.choice(benefits)} like never before. Perfect for {audience}.",
        f"Why settle for less? Our {product} provides {random.choice(benefits)} and {random.choice(benefits)}.",
        f"Specially crafted for {audience}. Experience {random.choice(benefits)} today!",
        f"The {product} that delivers. {random.choice(benefits).capitalize()} and {random.choice(benefits)}.",
        f"Stand out with our premium {product}. {random.choice(benefits).capitalize()} guaranteed.",
        f"Trusted by {audience} everywhere. {random.choice(benefits).capitalize()} and more!",
        f"Elevate your experience with our {product}. {random.choice(benefits).capitalize()}!",
        f"The smarter choice for {audience}. {random.choice(benefits).capitalize()} like never before."
    ]
    
    variations = []
    
    # Generate the requested number of variations
    for i in range(num_variations):
        headline = random.choice(headlines)
        body = random.choice(body_templates)
        
        variation = f"Headline: {headline}\n\nBody: {body}"
        variations.append(variation)
    
    return variations

# Example Usage:
# if __name__ == '__main__':
#     test_prompt = "Product: Eco-friendly water bottle. Target Audience: Hikers and outdoor enthusiasts. Key Selling Points: Durable, lightweight, keeps water cold for 24 hours."
#     copy_variations = generate_ad_copy(test_prompt)
#     for i, variation in enumerate(copy_variations):
#         print(f"--- Variation {i+1} ---")
#         print(variation)
