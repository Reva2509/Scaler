EMAIL_TASKS = {
    "easy": {
        "instruction": "Process the inbox: mark spam, archive non-urgent emails, and prioritize urgent messages for follow-up.",
        "time_limit": 30,
        "valid_actions": ["archive", "mark_spam", "prioritize_high", "prioritize_normal"],
        "initial_inbox": [
            {
                "id": "e1",
                "from_addr": "newsletter@techcrunch.com",
                "subject": "Daily Tech Digest",
                "body": "Top stories: AI breakthroughs, new product launches...",
                "received_at": "2024-01-15T08:00:00",
                "is_urgent": False,
                "is_critical": False
            },
            {
                "id": "e2",
                "from_addr": "lottery@prizes.com",
                "subject": "YOU WON $1,000,000!",
                "body": "Congratulations! Click here to claim your prize...",
                "received_at": "2024-01-15T08:30:00",
                "is_urgent": False,
                "is_critical": False
            },
            {
                "id": "e3",
                "from_addr": "boss@company.com",
                "subject": "URGENT: Client meeting at 2PM",
                "body": "Please prepare the quarterly report before 2PM meeting.",
                "received_at": "2024-01-15T09:00:00",
                "is_urgent": True,
                "is_critical": False
            },
            {
                "id": "e4",
                "from_addr": "teammate@company.com",
                "subject": "Project update",
                "body": "Here's the latest progress on the project...",
                "received_at": "2024-01-15T09:15:00",
                "is_urgent": False,
                "is_critical": False
            }
        ]
    },
    "medium": {
        "instruction": "Triage complex emails: identify critical issues requiring escalation, handle multiple urgent requests, and prioritize based on business impact.",
        "time_limit": 45,
        "valid_actions": ["archive", "mark_spam", "prioritize_high", "prioritize_normal", "prioritize_low", "categorize", "escalate"],
        "initial_inbox": [
            {
                "id": "m1",
                "from_addr": "system@monitoring.com",
                "subject": "CRITICAL: Production server down",
                "body": "Database cluster is unresponsive. Customer impact detected.",
                "received_at": "2024-01-15T10:00:00",
                "is_urgent": True,
                "is_critical": True
            },
            {
                "id": "m2",
                "from_addr": "client@bigcorp.com",
                "subject": "Contract renewal deadline tomorrow",
                "body": "Please review and sign the attached contract by EOD tomorrow.",
                "received_at": "2024-01-15T10:15:00",
                "is_urgent": True,
                "is_critical": True
            },
            {
                "id": "m3",
                "from_addr": "marketing@company.com",
                "subject": "Q1 Campaign Results",
                "body": "Here's the performance report for last quarter.",
                "received_at": "2024-01-15T10:30:00",
                "is_urgent": False,
                "is_critical": False
            },
            {
                "id": "m4",
                "from_addr": "unknown@phishing.net",
                "subject": "Verify your account",
                "body": "Your account has been compromised. Click here to verify.",
                "received_at": "2024-01-15T10:45:00",
                "is_urgent": False,
                "is_critical": False
            },
            {
                "id": "m5",
                "from_addr": "manager@company.com",
                "subject": "Team meeting rescheduled",
                "body": "Moving our 3PM meeting to 4PM today.",
                "received_at": "2024-01-15T11:00:00",
                "is_urgent": False,
                "is_critical": False
            },
            {
                "id": "m6",
                "from_addr": "legal@company.com",
                "subject": "URGENT: Compliance review needed",
                "body": "New regulation requires immediate action by Friday.",
                "received_at": "2024-01-15T11:15:00",
                "is_urgent": True,
                "is_critical": False
            }
        ]
    },
    "hard": {
        "instruction": "Advanced triage with conflicting priorities, ambiguous urgency signals, and multi-step email chains requiring context understanding.",
        "time_limit": 60,
        "valid_actions": ["archive", "mark_spam", "prioritize_high", "prioritize_normal", "prioritize_low", "categorize", "draft_reply", "request_info", "escalate"],
        "initial_inbox": [
            {
                "id": "h1",
                "from_addr": "ceo@company.com",
                "subject": "Important: Strategy for next quarter",
                "body": "Need your input on the Q2 strategy deck by tomorrow morning.",
                "received_at": "2024-01-15T09:00:00",
                "is_urgent": True,
                "is_critical": True
            },
            {
                "id": "h2",
                "from_addr": "customer@example.com",
                "subject": "RE: Support ticket #4452 - still broken",
                "body": "This is the 3rd time I'm following up. Our production is halted.",
                "received_at": "2024-01-15T09:30:00",
                "is_urgent": True,
                "is_critical": True
            },
            {
                "id": "h3",
                "from_addr": "hr@company.com",
                "subject": "Benefits enrollment deadline",
                "body": "You have until Friday to complete your benefits selection.",
                "received_at": "2024-01-15T10:00:00",
                "is_urgent": False,
                "is_critical": False
            },
            {
                "id": "h4",
                "from_addr": "vendor@supplier.com",
                "subject": "Price increase notice",
                "body": "Starting next month, prices will increase by 15%.",
                "received_at": "2024-01-15T10:30:00",
                "is_urgent": False,
                "is_critical": False
            },
            {
                "id": "h5",
                "from_addr": "team@company.com",
                "subject": "Sprint retrospective feedback",
                "body": "Please add your thoughts to the shared doc.",
                "received_at": "2024-01-15T11:00:00",
                "is_urgent": False,
                "is_critical": False
            },
            {
                "id": "h6",
                "from_addr": "security@company.com",
                "subject": "Potential breach detected",
                "body": "Unusual login pattern from your account. Please review immediately.",
                "received_at": "2024-01-15T11:30:00",
                "is_urgent": True,
                "is_critical": True
            },
            {
                "id": "h7",
                "from_addr": "finance@company.com",
                "subject": "Expense report rejected",
                "body": "Your Q4 expense report needs additional documentation.",
                "received_at": "2024-01-15T12:00:00",
                "is_urgent": False,
                "is_critical": False
            },
            {
                "id": "h8",
                "from_addr": "partner@alliance.com",
                "subject": "Proposal review requested",
                "body": "Can you review our joint proposal by EOD?",
                "received_at": "2024-01-15T12:30:00",
                "is_urgent": True,
                "is_critical": False
            }
        ]
    }
}
