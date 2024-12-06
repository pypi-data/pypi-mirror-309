# connector_few_shot_examples.py

connector_few_shot_examples = [
    {
        "user": ["Finance"],
        "assistant": {
            "connectors": ["plaid", "mint", "vanguard", "personal_capital"]
        }
    },
    {
        "user": ["Banking"],
        "assistant": {
            "connectors": ["chase", "wells_fargo", "bank_of_america", "citibank"]
        }
    },
    {
        "user": ["Payments"],
        "assistant": {
            "connectors": ["paypal", "stripe", "square", "adyen"]
        }
    },
    {
        "user": ["Cryptocurrency"],
        "assistant": {
            "connectors": ["coinbase", "binance", "kraken", "gemini"]
        }
    },
    {
        "user": ["Accounting"],
        "assistant": {
            "connectors": ["quickbooks", "xero", "freshbooks", "sage"]
        }
    },
    {
        "user": ["Communication"],
        "assistant": {
            "connectors": ["twilio", "vonage", "ringcentral", "zoom_phone"]
        }
    },
    {
        "user": ["Messaging"],
        "assistant": {
            "connectors": ["slack", "microsoft_teams", "whatsapp", "signal"]
        }
    },
    {
        "user": ["Email"],
        "assistant": {
            "connectors": ["gmail", "outlook", "mailchimp", "sendgrid"]
        }
    },
    {
        "user": ["VideoStreaming"],
        "assistant": {
            "connectors": ["youtube", "vimeo", "twitch", "dailymotion"]
        }
    },
    {
        "user": ["VideoConferencing"],
        "assistant": {
            "connectors": ["zoom", "google_meet", "microsoft_teams", "webex"]
        }
    },
    {
        "user": ["SocialMedia"],
        "assistant": {
            "connectors": ["facebook", "twitter", "instagram", "linkedin"]
        }
    },
    {
        "user": ["Ecommerce"],
        "assistant": {
            "connectors": ["shopify", "bigcommerce", "magento", "woocommerce"]
        }
    },
    {
        "user": ["Marketplaces"],
        "assistant": {
            "connectors": ["amazon", "ebay", "etsy", "alibaba"]
        }
    },
    {
        "user": ["InventoryManagement"],
        "assistant": {
            "connectors": ["netsuite", "zoho_inventory", "dearsystems", "tradegecko"]
        }
    },
    {
        "user": ["OrderManagement"],
        "assistant": {
            "connectors": ["shopify_orders", "salesforce_order_management", "oracle_om", "magento_orders"]
        }
    },
    {
        "user": ["Healthcare"],
        "assistant": {
            "connectors": ["epic", "cerner", "athenahealth", "allscripts"]
        }
    },
    {
        "user": ["Travel"],
        "assistant": {
            "connectors": ["expedia", "booking_com", "amadeus", "skyscanner"]
        }
    },
    {
        "user": ["Transportation"],
        "assistant": {
            "connectors": ["uber", "lyft", "google_maps", "transit"]
        }
    },
    {
        "user": ["Education"],
        "assistant": {
            "connectors": ["canvas", "blackboard", "moodle", "google_classroom"]
        }
    },
    {
        "user": ["Entertainment"],
        "assistant": {
            "connectors": ["netflix", "hulu", "spotify", "disney_plus"]
        }
    },
    {
        "user": ["MusicStreaming"],
        "assistant": {
            "connectors": ["spotify", "apple_music", "pandora", "tidal"]
        }
    },
    {
        "user": ["Gaming"],
        "assistant": {
            "connectors": ["steam", "xbox_live", "playstation_network", "epic_games"]
        }
    },
    {
        "user": ["Productivity"],
        "assistant": {
            "connectors": ["notion", "asana", "trello", "monday"]
        }
    },
    {
        "user": ["TaskManagement"],
        "assistant": {
            "connectors": ["todoist", "microsoft_planner", "clickup", "google_tasks"]
        }
    },
    {
        "user": ["DocumentManagement"],
        "assistant": {
            "connectors": ["google_drive", "dropbox", "box", "onedrive"]
        }
    },
    {
        "user": ["Geolocation"],
        "assistant": {
            "connectors": ["google_maps", "here", "mapbox", "openstreetmap"]
        }
    },
    {
        "user": ["InternetOfThings"],
        "assistant": {
            "connectors": ["smartthings", "philips_hue", "nest", "ifttt"]
        }
    },
    {
        "user": ["MachineLearning"],
        "assistant": {
            "connectors": ["tensorflow", "pytorch", "scikit_learn", "keras"]
        }
    },
    {
        "user": ["ArtificialIntelligence"],
        "assistant": {
            "connectors": ["openai", "ibm_watson", "google_ai", "azure_ai"]
        }
    },
    {
        "user": ["DataStorage"],
        "assistant": {
            "connectors": ["amazon_s3", "google_cloud_storage", "azure_blob", "backblaze"]
        }
    },
    {
        "user": ["Databases"],
        "assistant": {
            "connectors": ["mysql", "postgresql", "mongodb", "oracle_db"]
        }
    },
    {
        "user": ["FileStorage"],
        "assistant": {
            "connectors": ["dropbox", "box", "google_drive", "icloud"]
        }
    },
    {
        "user": ["Analytics"],
        "assistant": {
            "connectors": ["google_analytics", "mixpanel", "tableau", "power_bi"]
        }
    },
    {
        "user": ["Marketing"],
        "assistant": {
            "connectors": ["hubspot", "marketo", "mailchimp", "pardot"]
        }
    },
    {
        "user": ["Security"],
        "assistant": {
            "connectors": ["auth0", "okta", "duo", "microsoft_azure_ad"]
        }
    },
    {
        "user": ["HumanResources"],
        "assistant": {
            "connectors": ["workday", "bamboohr", "sap_successfactors", "adp"]
        }
    },
    {
        "user": ["CustomerSupport"],
        "assistant": {
            "connectors": ["zendesk", "freshdesk", "intercom", "helpscout"]
        }
    },
    {
        "user": ["ContentManagement"],
        "assistant": {
            "connectors": ["wordpress", "drupal", "contentful", "sitecore"]
        }
    },
    {
        "user": ["RealEstate"],
        "assistant": {
            "connectors": ["zillow", "realtor_com", "redfin", "mls"]
        }
    },
    {
        "user": ["Legal"],
        "assistant": {
            "connectors": ["docusign", "clio", "lawpay", "lexisnexis"]
        }
    },
    {
        "user": ["News"],
        "assistant": {
            "connectors": ["newsapi", "new_york_times", "bbc", "reuters"]
        }
    },
    {
        "user": ["Weather"],
        "assistant": {
            "connectors": ["openweathermap", "weatherstack", "accuweather", "weatherbit"]
        }
    },
    {
        "user": ["Utilities"],
        "assistant": {
            "connectors": ["pg_e", "duke_energy", "con_edison", "national_grid"]
        }
    },
    {
        "user": ["Telecommunications"],
        "assistant": {
            "connectors": ["at_t", "verizon", "t_mobile", "sprint"]
        }
    },
    {
        "user": ["Blockchain"],
        "assistant": {
            "connectors": ["infura", "alchemy", "etherscan", "blockcypher"]
        }
    },
    {
        "user": ["Government"],
        "assistant": {
            "connectors": ["data_gov", "census_gov", "irs", "usa_gov"]
        }
    },
    {
        "user": ["Energy"],
        "assistant": {
            "connectors": ["tesla_powerwall", "enphase", "solaredge", "bloom_energy"]
        }
    },
    {
        "user": ["Manufacturing"],
        "assistant": {
            "connectors": ["sap", "siemens", "ge_digital", "rockwell_automation"]
        }
    },
    {
        "user": ["Automotive"],
        "assistant": {
            "connectors": ["onstar", "fordpass", "toyota_connect", "bmw_connected"]
        }
    },
    {
        "user": ["Media"],
        "assistant": {
            "connectors": ["brightcove", "adobe_experience_manager", "kaltura", "jw_player"]
        }
    },
    {
        "user": ["Advertising"],
        "assistant": {
            "connectors": ["google_ads", "facebook_ads", "linkedin_ads", "bing_ads"]
        }
    },
    {
        "user": ["AugmentedReality"],
        "assistant": {
            "connectors": ["arkit", "arcore", "vuforia", "8th_wall"]
        }
    },
    {
        "user": ["VirtualReality"],
        "assistant": {
            "connectors": ["oculus", "htc_vive", "steamvr", "unity_vr"]
        }
    },
    {
        "user": ["Survey"],
        "assistant": {
            "connectors": ["surveymonkey", "typeform", "google_forms", "qualtrics"]
        }
    },
    {
        "user": ["BlockchainExchanges"],
        "assistant": {
            "connectors": ["coinbase_pro", "binance", "kraken", "bitstamp"]
        }
    },
    {
        "user": ["FinancialData"],
        "assistant": {
            "connectors": ["bloomberg", "yahoo_finance", "morningstar", "alpha_vantage"]
        }
    },
    {
        "user": ["BlockchainSmartContracts"],
        "assistant": {
            "connectors": ["etherscan", "truffle", "hardhat", "infura"]
        }
    },
    {
        "user": ["FoodDelivery"],
        "assistant": {
            "connectors": ["ubereats", "doordash", "grubhub", "postmates"]
        }
    },
    {
        "user": ["Logistics"],
        "assistant": {
            "connectors": ["fedex", "dhl", "ups", "usps"]
        }
    },
    {
        "user": ["EventManagement"],
        "assistant": {
            "connectors": ["eventbrite", "meetup", "cvent", "ticketmaster"]
        }
    },
    {
        "user": ["RecommendationSystems"],
        "assistant": {
            "connectors": ["amazon_personalize", "recombee", "google_recommendations_ai", "salesforce_einstein"]
        }
    },
    {
        "user": ["Retail"],
        "assistant": {
            "connectors": ["square_pos", "shopify_pos", "lightspeed", "vend"]
        }
    },
    {
        "user": ["LoyaltyPrograms"],
        "assistant": {
            "connectors": ["fivestars", "loyaltylion", "perkville", "yotpo"]
        }
    },
    {
        "user": ["Search"],
        "assistant": {
            "connectors": ["elasticsearch", "algolia", "azure_search", "solr"]
        }
    },
    {
        "user": ["DataVisualization"],
        "assistant": {
            "connectors": ["d3_js", "chart_js", "highcharts", "plotly"]
        }
    },
    {
        "user": ["CatchAll"],
        "assistant": {
            "connectors": ["custom_api", "zapier", "ifttt", "integrately"]
        }
    }
]
