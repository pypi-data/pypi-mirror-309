# operation_selection_few_shot.py

operation_few_shot_examples = [
    {
        "user": "What’s my current balance across all my accounts?",
        "connector": "plaid",
        "assistant": {
            "operation": "get_account_balance"
        }
    },
    {
        "user": "Schedule a meeting with my manager tomorrow at 3 PM.",
        "connector": "microsoft_outlook",
        "assistant": {
            "operation": "create_event"
        }
    },
    {
        "user": "Send a thank-you email to the recent customer inquiries.",
        "connector": "zendesk",
        "assistant": {
            "operation": "send_response"
        }
    },
    {
        "user": "List today’s top-selling products.",
        "connector": "shopify",
        "assistant": {
            "operation": "get_top_selling_products"
        }
    },
    {
        "user": "Find nearby hotels with available rooms tonight.",
        "connector": "airbnb",
        "assistant": {
            "operation": "search_nearby_hotels"
        }
    }
]
