# categories.py

category_few_shot_examples = [
    {
        "category": "Finance",
        "description": "APIs related to financial services, including banking, payments, investments, and personal finance management.",
        "examples": [
            # Highly specific
            "What's the current balance of my investment portfolio at Vanguard?",
            # Somewhat specific
            "Show me my financial summary for this month.",
            # Very generic
            "I need help organizing my money.",
            # Example mentioning APIs (without explicitly saying 'API' unless natural)
            "Connect to Plaid to link all my bank accounts.",
            "Use the Mint integration to analyze my spending habits."
        ]
    },
    {
        "category": "Banking",
        "description": "APIs for managing bank accounts, viewing transactions, transferring funds, and integrating with banking institutions.",
        "examples": [
            "Transfer $500 from my checking account at Chase to my savings account.",
            "View the last five transactions on my Wells Fargo account.",
            "I need to check my account balances.",
            "Use the Bank of America service to pay my credit card bill.",
            "Access my account details through the CitiBank integration."
        ]
    },
    {
        "category": "Payments",
        "description": "APIs facilitating payment processing, invoicing, billing, and payment gateway integrations.",
        "examples": [
            "Send a $50 payment to John Doe via PayPal.",
            "Process an invoice for client ABC Corp.",
            "I need to make a payment.",
            "Charge a customer using the Stripe service.",
            "Initiate a transaction through Square."
        ]
    },
    {
        "category": "Cryptocurrency",
        "description": "APIs for interacting with cryptocurrency wallets, exchanges, and blockchain operations.",
        "examples": [
            "Transfer 0.5 BTC from my Coinbase wallet to my Ledger Nano S.",
            "What's the current price of Ethereum?",
            "I want to trade digital currencies.",
            "Connect to Binance to buy some Dogecoin.",
            "Use Kraken to check my crypto portfolio."
        ]
    },
    {
        "category": "Accounting",
        "description": "APIs for bookkeeping, expense tracking, and financial reporting systems.",
        "examples": [
            "Record a $200 office supplies expense in QuickBooks.",
            "Generate my company's financial statements for Q2.",
            "I need to organize my business expenses.",
            "Use Xero to reconcile my bank transactions.",
            "Integrate with FreshBooks to manage client invoices."
        ]
    },
    {
        "category": "Communication",
        "description": "APIs for voice calls, telephony services, and real-time communication systems.",
        "examples": [
            "Set up a conference call with the team.",
            "Call my client using VoIP.",
            "I need to communicate with someone.",
            "Utilize Twilio to send a voice message.",
            "Connect through Zoom for a voice call."
        ]
    },
    {
        "category": "Messaging",
        "description": "APIs for sending and receiving text-based messages, including SMS, instant messaging, and notifications.",
        "examples": [
            "Send a text message to Sarah about the meeting.",
            "Notify all users about the system update.",
            "I want to send a message.",
            "Use Slack to message the marketing channel.",
            "Send an SMS via Nexmo to all subscribers."
        ]
    },
    {
        "category": "Email",
        "description": "APIs for email services, including sending, receiving, and email marketing automation.",
        "examples": [
            "Compose and send an email to the sales team.",
            "Check for new messages in my inbox.",
            "I need to send some emails.",
            "Send a newsletter using Mailchimp.",
            "Integrate with Gmail to manage my emails."
        ]
    },
    {
        "category": "VideoStreaming",
        "description": "APIs for streaming video content over the internet, such as live broadcasts and on-demand video services.",
        "examples": [
            "Start a live video stream for the event.",
            "Play the latest episode of my favorite show.",
            "I want to watch something.",
            "Stream content using YouTube Live.",
            "Access on-demand videos through Netflix."
        ]
    },
    {
        "category": "VideoConferencing",
        "description": "APIs for real-time video communication, video calls, and online conferencing services.",
        "examples": [
            "Schedule a video conference with the project team.",
            "Join the ongoing meeting with my webcam.",
            "I need to have a video call.",
            "Connect via Zoom for our weekly sync.",
            "Use Microsoft Teams for the client meeting."
        ]
    },
    {
        "category": "SocialMedia",
        "description": "APIs for interacting with social media platforms, posting content, and accessing social data.",
        "examples": [
            "Post a new update to our company's Twitter account.",
            "Check the latest comments on our Facebook page.",
            "I want to engage with our followers.",
            "Use Instagram to share a new product photo.",
            "Access LinkedIn to view recent connection requests."
        ]
    },
    {
        "category": "Ecommerce",
        "description": "APIs for online store management, including product catalogs, orders, and customer data.",
        "examples": [
            "Add a new product to our Shopify store.",
            "Process an order placed by a customer.",
            "I need to manage our online store.",
            "Integrate with WooCommerce to update inventory.",
            "Use Magento to analyze sales data."
        ]
    },
    {
        "category": "Marketplaces",
        "description": "APIs for managing multi-vendor marketplaces, auctions, and product listings across platforms.",
        "examples": [
            "List a new item for sale on Amazon Marketplace.",
            "Update pricing for our eBay listings.",
            "I want to manage our marketplace products.",
            "Use Etsy integration to track sales.",
            "Connect to Alibaba to source new products."
        ]
    },
    {
        "category": "InventoryManagement",
        "description": "APIs for tracking and managing product inventory across multiple locations and warehouses.",
        "examples": [
            "Update stock levels for item SKU123 in warehouse A.",
            "Generate a report on current inventory levels.",
            "I need to check our product quantities.",
            "Integrate with SAP to manage inventory data.",
            "Use Oracle Netsuite to reorder low-stock items."
        ]
    },
    {
        "category": "OrderManagement",
        "description": "APIs for processing, tracking, and managing customer orders within e-commerce systems.",
        "examples": [
            "Process a refund for order #4567.",
            "Update the shipping status of order #1234.",
            "I need to handle customer orders.",
            "Use Salesforce to manage order fulfillment.",
            "Connect to ShipStation to print shipping labels."
        ]
    },
    {
        "category": "Healthcare",
        "description": "APIs for managing patient data, electronic health records, telemedicine, and healthcare services.",
        "examples": [
            "Schedule an appointment with Dr. Smith for next Tuesday.",
            "Access my medical test results from last week.",
            "I need to manage patient information.",
            "Use Epic Systems to update patient records.",
            "Integrate with Cerner to view EHR data."
        ]
    },
    {
        "category": "Travel",
        "description": "APIs for flight, hotel, and travel booking services, including itinerary management.",
        "examples": [
            "Book a flight from New York to London on December 15th.",
            "Find hotel availability in Paris for next weekend.",
            "I want to plan a trip.",
            "Use Expedia to compare flight prices.",
            "Connect to Booking.com to reserve accommodations."
        ]
    },
    {
        "category": "Transportation",
        "description": "APIs for public transport data, ride-sharing services, and route planning functionalities.",
        "examples": [
            "Order an Uber to the airport.",
            "Check the next bus arrival time at my stop.",
            "I need to get somewhere.",
            "Use Lyft to schedule a ride.",
            "Access Google Maps to find the fastest route."
        ]
    },
    {
        "category": "Education",
        "description": "APIs for educational platforms, learning management systems, and student data management.",
        "examples": [
            "Enroll in the online Python programming course.",
            "Access my grades for the last semester.",
            "I want to learn something new.",
            "Integrate with Canvas LMS to submit assignments.",
            "Use Coursera to browse available courses."
        ]
    },
    {
        "category": "Entertainment",
        "description": "APIs for media streaming, gaming services, and interactive entertainment platforms.",
        "examples": [
            "Play the latest album by my favorite artist.",
            "Find new movies to watch this weekend.",
            "I need something fun to do.",
            "Use Spotify to create a new playlist.",
            "Connect to Steam to download a game."
        ]
    },
    {
        "category": "MusicStreaming",
        "description": "APIs for streaming music content and managing audio libraries.",
        "examples": [
            "Stream 'Blinding Lights' by The Weeknd.",
            "Add 'Classical Essentials' to my library.",
            "I want to listen to music.",
            "Use Apple Music to find new releases.",
            "Access my playlists through Pandora."
        ]
    },
    {
        "category": "Gaming",
        "description": "APIs for game development, multiplayer functionalities, and gaming platform integrations.",
        "examples": [
            "Join a multiplayer match in Call of Duty.",
            "Check my achievements on Xbox Live.",
            "I want to play a game.",
            "Use the Unity engine to develop a new game level.",
            "Integrate with PlayStation Network to access friends list."
        ]
    },
    {
        "category": "Productivity",
        "description": "APIs for task management, project management, and productivity tools.",
        "examples": [
            "Create a new task for completing the budget report.",
            "Update the project timeline in Asana.",
            "I need to organize my work.",
            "Use Trello to manage my projects.",
            "Integrate with Notion to take notes."
        ]
    },
    {
        "category": "TaskManagement",
        "description": "APIs for managing to-do lists, tasks, and project workflows.",
        "examples": [
            "Add 'Buy groceries' to my to-do list.",
            "Set a reminder for the team meeting tomorrow.",
            "I need to keep track of my tasks.",
            "Use Todoist to prioritize my daily activities.",
            "Connect with Microsoft Planner to assign tasks."
        ]
    },
    {
        "category": "DocumentManagement",
        "description": "APIs for handling document creation, storage, sharing, and collaboration.",
        "examples": [
            "Share the Q3 financial report with the finance team.",
            "Edit the project proposal document.",
            "I need to work on some files.",
            "Use Google Drive to access shared documents.",
            "Integrate with Dropbox to sync my files."
        ]
    },
    {
        "category": "Geolocation",
        "description": "APIs for location tracking, mapping services, distance calculations, and geographic data.",
        "examples": [
            "Find the nearest coffee shop to my current location.",
            "Calculate the distance between New York and Los Angeles.",
            "Where am I?",
            "Use Google Maps API to display a map.",
            "Access OpenStreetMap data for routing."
        ]
    },
    {
        "category": "InternetOfThings",
        "description": "APIs for managing IoT devices, sensor data, and device communication protocols.",
        "examples": [
            "Turn on the living room lights.",
            "Check the temperature readings from the office sensors.",
            "I want to control my devices.",
            "Use Philips Hue integration to adjust lighting.",
            "Connect to Nest thermostat to set the temperature."
        ]
    },
    {
        "category": "MachineLearning",
        "description": "APIs for implementing machine learning models, data analysis, and artificial intelligence services.",
        "examples": [
            "Predict sales trends for the next quarter.",
            "Analyze customer data to find buying patterns.",
            "I need insights from my data.",
            "Use TensorFlow to build a predictive model.",
            "Integrate with Scikit-learn for data classification."
        ]
    },
    {
        "category": "ArtificialIntelligence",
        "description": "APIs for AI functionalities such as natural language processing, computer vision, and cognitive services.",
        "examples": [
            "Translate this text from English to Spanish.",
            "Recognize objects in this image.",
            "I need smart features.",
            "Use OpenAI's GPT-3 to generate text.",
            "Integrate with IBM Watson for sentiment analysis."
        ]
    },
    {
        "category": "DataStorage",
        "description": "APIs for cloud storage solutions, file management, and data retrieval systems.",
        "examples": [
            "Upload these files to my cloud storage.",
            "Retrieve the backup from last week.",
            "I need to store some data.",
            "Use Amazon S3 to manage my data buckets.",
            "Connect to Google Cloud Storage for file access."
        ]
    },
    {
        "category": "Databases",
        "description": "APIs for interacting with database systems, performing CRUD operations, and managing data schemas.",
        "examples": [
            "Insert a new record into the customer table.",
            "Update the address field for user ID 123.",
            "I need to manage my database.",
            "Use MongoDB to store user profiles.",
            "Connect to MySQL to run queries."
        ]
    },
    {
        "category": "FileStorage",
        "description": "APIs for uploading, downloading, and managing files in cloud storage services.",
        "examples": [
            "Download the latest version of the project document.",
            "Delete unnecessary files from storage.",
            "I need to manage my files.",
            "Use Dropbox to share files with the team.",
            "Access OneDrive to organize my folders."
        ]
    },
    {
        "category": "Analytics",
        "description": "APIs for data analytics, business intelligence, and reporting services.",
        "examples": [
            "Generate a sales performance report for Q4.",
            "Analyze website traffic for the past month.",
            "I need insights into our performance.",
            "Use Google Analytics to track user behavior.",
            "Integrate with Tableau for data visualization."
        ]
    },
    {
        "category": "Marketing",
        "description": "APIs for marketing automation, campaign management, and customer engagement tools.",
        "examples": [
            "Send out an email campaign to all subscribers.",
            "Schedule social media posts for the week.",
            "I want to reach more customers.",
            "Use HubSpot to manage marketing activities.",
            "Connect to Mailchimp to send newsletters."
        ]
    },
    {
        "category": "Security",
        "description": "APIs for authentication, authorization, encryption, and other security-related services.",
        "examples": [
            "Enable two-factor authentication for my account.",
            "Encrypt sensitive data before storage.",
            "I need to secure my application.",
            "Use Auth0 for user authentication.",
            "Integrate with Okta for single sign-on."
        ]
    },
    {
        "category": "HumanResources",
        "description": "APIs for managing employee data, payroll, recruitment, and HR processes.",
        "examples": [
            "Add a new employee to the HR system.",
            "Process payroll for this pay period.",
            "I need to manage our staff records.",
            "Use Workday to update employee information.",
            "Integrate with BambooHR for time-off requests."
        ]
    },
    {
        "category": "CustomerSupport",
        "description": "APIs for handling customer inquiries, support tickets, and helpdesk functionalities.",
        "examples": [
            "Create a new support ticket for a customer issue.",
            "Update the status of ticket #789 to resolved.",
            "I need to assist our clients.",
            "Use Zendesk to manage support tickets.",
            "Connect to Freshdesk for customer interactions."
        ]
    },
    {
        "category": "ContentManagement",
        "description": "APIs for managing digital content, including creation, editing, and publishing workflows.",
        "examples": [
            "Publish a new blog post on our website.",
            "Edit the homepage content to reflect the new promotion.",
            "I need to update our site.",
            "Use WordPress API to manage site content.",
            "Integrate with Drupal for content updates."
        ]
    },
    {
        "category": "RealEstate",
        "description": "APIs for property listings, real estate transactions, and property management services.",
        "examples": [
            "List a new property for sale in Los Angeles.",
            "Search for rental properties under $2000/month.",
            "I'm looking for a place to live.",
            "Use Zillow to find housing market data.",
            "Connect with Realtor.com for property listings."
        ]
    },
    {
        "category": "Legal",
        "description": "APIs for legal services, contract management, compliance systems, and regulatory data.",
        "examples": [
            "Draft a non-disclosure agreement for a new partner.",
            "Review the compliance requirements for data privacy.",
            "I need legal assistance.",
            "Use DocuSign to send a contract for signature.",
            "Integrate with Clio for case management."
        ]
    },
    {
        "category": "News",
        "description": "APIs for accessing news articles, headlines, and media content from various sources.",
        "examples": [
            "Show me the latest headlines in technology.",
            "Get news updates on the stock market.",
            "I want to read something interesting.",
            "Use the New York Times API to fetch articles.",
            "Connect to BBC News for global updates."
        ]
    },
    {
        "category": "Weather",
        "description": "APIs for retrieving weather data, forecasts, climate information, and meteorological services.",
        "examples": [
            "What's the weather forecast for tomorrow in Chicago?",
            "Alert me if it's going to rain today.",
            "How's the weather?",
            "Use OpenWeatherMap to get current conditions.",
            "Access Weather Underground for detailed forecasts."
        ]
    },
    {
        "category": "Utilities",
        "description": "APIs for utility services, including electricity, water, gas management systems, and related data.",
        "examples": [
            "Pay my electricity bill due next week.",
            "Check my water usage for this month.",
            "I need to manage my utilities.",
            "Use PG&E integration to view energy consumption.",
            "Connect to Con Edison to set up autopay."
        ]
    },
    {
        "category": "Telecommunications",
        "description": "APIs for telecom services, including mobile network management, SMS gateways, and telephony integrations.",
        "examples": [
            "Check my mobile data usage for this billing cycle.",
            "Add international calling to my phone plan.",
            "I need to manage my phone services.",
            "Use AT&T to view my account details.",
            "Integrate with Verizon for billing information."
        ]
    },
    {
        "category": "Blockchain",
        "description": "APIs for blockchain interactions, smart contract management, and decentralized application support.",
        "examples": [
            "Deploy a smart contract on the Ethereum network.",
            "Check the status of a transaction hash.",
            "I want to work with blockchain technology.",
            "Use Infura to interact with the blockchain.",
            "Connect with MetaMask to access my wallet."
        ]
    },
    {
        "category": "Government",
        "description": "APIs for government services, public data access, regulatory compliance, and civic engagement platforms.",
        "examples": [
            "Find the nearest DMV office.",
            "Access census data for demographic analysis.",
            "I need official information.",
            "Use Data.gov to retrieve public datasets.",
            "Connect to the IRS for tax transcripts."
        ]
    },
    {
        "category": "Energy",
        "description": "APIs for energy management, renewable energy systems, and utility data services.",
        "examples": [
            "Monitor solar panel energy production.",
            "Check my home's energy efficiency rating.",
            "I want to save on energy costs.",
            "Use Tesla's Powerwall to track energy storage.",
            "Integrate with Enphase to manage solar systems."
        ]
    },
    {
        "category": "Manufacturing",
        "description": "APIs for manufacturing processes, supply chain management, production systems, and automation.",
        "examples": [
            "Schedule maintenance for production line machinery.",
            "Order raw materials for next month's production.",
            "I need to optimize our factory operations.",
            "Use SAP ERP to manage supply chain data.",
            "Integrate with Siemens automation systems."
        ]
    },
    {
        "category": "Automotive",
        "description": "APIs for vehicle data, automotive services, fleet management, and transportation systems.",
        "examples": [
            "Locate my car using GPS tracking.",
            "Schedule a service appointment for my vehicle.",
            "I need information about my car.",
            "Use OnStar to access vehicle diagnostics.",
            "Connect with Uber Fleet to manage drivers."
        ]
    },
    {
        "category": "Media",
        "description": "APIs for media content management, publishing platforms, and digital asset handling.",
        "examples": [
            "Upload a new video to our media library.",
            "Edit metadata for the latest podcast episode.",
            "I need to manage our digital content.",
            "Use Brightcove to host video content.",
            "Integrate with Adobe Experience Manager for assets."
        ]
    },
    {
        "category": "Advertising",
        "description": "APIs for digital advertising, ad campaign management, and programmatic advertising services.",
        "examples": [
            "Launch a new ad campaign targeting millennials.",
            "Analyze the performance of our latest ads.",
            "I want to promote our products.",
            "Use Google Ads to set up PPC campaigns.",
            "Connect to Facebook Ads Manager for audience insights."
        ]
    },
    {
        "category": "AugmentedReality",
        "description": "APIs for developing augmented reality applications, object recognition, and spatial mapping.",
        "examples": [
            "Overlay product information onto real-world images.",
            "Develop an AR experience for our new app.",
            "I want to enhance reality.",
            "Use ARKit to create an interactive feature.",
            "Integrate with Vuforia for object tracking."
        ]
    },
    {
        "category": "VirtualReality",
        "description": "APIs for creating virtual reality experiences, immersive environments, and VR hardware integrations.",
        "examples": [
            "Build a virtual showroom for our products.",
            "Create a VR training simulation for employees.",
            "I need to design immersive content.",
            "Use Oculus SDK to develop VR applications.",
            "Integrate with HTC Vive for virtual experiences."
        ]
    },
    {
        "category": "Survey",
        "description": "APIs for creating, distributing, and analyzing surveys and questionnaires.",
        "examples": [
            "Send out a customer satisfaction survey.",
            "Analyze responses from the recent employee poll.",
            "I want to gather feedback.",
            "Use SurveyMonkey to create a new survey.",
            "Integrate with Typeform for data collection."
        ]
    },
    {
        "category": "BlockchainExchanges",
        "description": "APIs for cryptocurrency exchanges, trading platforms, and market data services.",
        "examples": [
            "Place a buy order for 2 ETH on Coinbase Pro.",
            "Check the order book for BTC/USD on Binance.",
            "I want to trade cryptocurrencies.",
            "Use Kraken to execute a market trade.",
            "Access real-time prices through Bitstamp."
        ]
    },
    {
        "category": "FinancialData",
        "description": "APIs for accessing financial market data, stock prices, and economic indicators.",
        "examples": [
            "Get the latest stock price for Apple Inc.",
            "Retrieve historical data for the S&P 500 index.",
            "I need market information.",
            "Use Bloomberg API to access financial news.",
            "Connect to Yahoo Finance for stock analysis."
        ]
    },
    {
        "category": "BlockchainSmartContracts",
        "description": "APIs for deploying, managing, and interacting with smart contracts on blockchain platforms.",
        "examples": [
            "Audit a smart contract for security vulnerabilities.",
            "Interact with a DeFi protocol on Ethereum.",
            "I need to work with smart contracts.",
            "Use Etherscan to verify contract code.",
            "Connect with Truffle Suite for contract development."
        ]
    },
    {
        "category": "FoodDelivery",
        "description": "APIs for on-demand food delivery services, including restaurant listings and delivery logistics.",
        "examples": [
            "Order a pizza from the nearest Domino's.",
            "Track my food delivery order status.",
            "I'm hungry.",
            "Use Uber Eats to find nearby restaurants.",
            "Connect to Grubhub to reorder my last meal."
        ]
    },
    {
        "category": "Logistics",
        "description": "APIs for managing supply chains, shipping, freight, and delivery tracking.",
        "examples": [
            "Schedule a pickup for a package shipment.",
            "Track the delivery status of order #9876.",
            "I need to manage shipments.",
            "Use FedEx API to print shipping labels.",
            "Integrate with DHL for international freight."
        ]
    },
    {
        "category": "EventManagement",
        "description": "APIs for event ticketing, scheduling, and event management platforms.",
        "examples": [
            "Create an event registration page for our conference.",
            "Sell tickets online for the upcoming concert.",
            "I want to organize an event.",
            "Use Eventbrite to manage attendee registrations.",
            "Integrate with Meetup to schedule group events."
        ]
    },
    {
        "category": "RecommendationSystems",
        "description": "APIs for providing personalized content and product recommendations based on user behavior.",
        "examples": [
            "Suggest products similar to what I've viewed.",
            "Provide movie recommendations based on my watch history.",
            "I need some suggestions.",
            "Use Amazon Personalize to enhance recommendations.",
            "Integrate with Netflix to generate personalized lists."
        ]
    },
    {
        "category": "Retail",
        "description": "APIs for managing retail operations, inventory, and in-store services.",
        "examples": [
            "Update the point-of-sale system with new pricing.",
            "Check inventory levels across all store locations.",
            "I need to manage my retail business.",
            "Use Square to process in-store transactions.",
            "Integrate with Shopify POS for sales data."
        ]
    },
    {
        "category": "LoyaltyPrograms",
        "description": "APIs for managing customer loyalty programs, points, rewards, and incentives.",
        "examples": [
            "Enroll a customer into the loyalty program.",
            "Redeem points for a discount on the next purchase.",
            "I want to reward my customers.",
            "Use Fivestars to track loyalty points.",
            "Integrate with LoyaltyLion for rewards management."
        ]
    },
    {
        "category": "Search",
        "description": "APIs for performing search operations, indexing, and query functionality.",
        "examples": [
            "Search for all documents containing 'Q1 report'.",
            "Implement autocomplete functionality on the website.",
            "I need to find something.",
            "Use Elasticsearch to index data.",
            "Integrate with Algolia for fast search results."
        ]
    },
    {
        "category": "DataVisualization",
        "description": "APIs for creating charts, graphs, and other visual data representations.",
        "examples": [
            "Generate a bar chart of monthly sales figures.",
            "Visualize user engagement metrics over time.",
            "I need to see data trends.",
            "Use D3.js to create interactive graphs.",
            "Integrate with Chart.js for data plotting."
        ]
    },
    {
        "category": "CatchAll",
        "description": "APIs that do not fit into any specific category, covering miscellaneous or emerging use cases.",
        "examples": [
            "Perform a task that doesn't fit elsewhere.",
            "Handle a unique request for my application.",
            "I need help with something unusual.",
            "Use a custom API to solve a specific problem.",
            "Integrate with a new service for experimental features."
        ]
    }
]
