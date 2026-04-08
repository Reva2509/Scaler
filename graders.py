from typing import List, Dict, Any

class EmailTriageGrader:
    def __init__(self, task_id: str):
        self.task_id = task_id
    
    def grade(self, triage_log: List[Dict], task_config: Dict) -> float:
        """Programmatic grader returning score between 0.0 and 1.0."""
        if not triage_log:
            return 0.0
        
        total_score = 0.0
        max_score = 0.0
        
        # Grading criteria based on task difficulty
        if self.task_id == "easy":
            criteria = self._easy_criteria()
        elif self.task_id == "medium":
            criteria = self._medium_criteria()
        else:
            criteria = self._hard_criteria()
        
        # Score each action
        for i, action_entry in enumerate(triage_log):
            action = action_entry["action"]
            email_id = action_entry["email_id"]
            
            # Find email context
            email = self._find_email_by_id(email_id, task_config["initial_inbox"])
            if not email:
                continue
            
            # Apply criteria weights
            for criterion_name, criterion_func in criteria.items():
                weight = criterion_func.get("weight", 1.0)
                score = criterion_func["evaluator"](action, email, i, triage_log)
                total_score += score * weight
                max_score += weight
        
        return min(1.0, total_score / max_score) if max_score > 0 else 0.0
    
    def _easy_criteria(self):
        """Simple criteria for easy task."""
        return {
            "spam_handling": {
                "weight": 2.0,
                "evaluator": lambda action, email, idx, log: 1.0 if "spam" in email["body"].lower() and action == "mark_spam" else (0.0 if "spam" in email["body"].lower() else 0.5)
            },
            "urgency_handling": {
                "weight": 2.0,
                "evaluator": lambda action, email, idx, log: 1.0 if email["is_urgent"] and action in ["prioritize_high", "draft_reply"] else (0.0 if email["is_urgent"] and action in ["archive", "mark_spam"] else 0.5)
            },
            "efficiency": {
                "weight": 1.0,
                "evaluator": lambda action, email, idx, log: 1.0 if idx < 5 else 0.5
            }
        }
    
    def _medium_criteria(self):
        """More nuanced criteria for medium task."""
        return {
            "critical_escalation": {
                "weight": 3.0,
                "evaluator": lambda action, email, idx, log: 1.0 if email["is_critical"] and action == "escalate" else (0.0 if email["is_critical"] and action in ["archive", "mark_spam"] else 0.3)
            },
            "phishing_detection": {
                "weight": 2.0,
                "evaluator": lambda action, email, idx, log: 1.0 if "phishing" in email["body"].lower() and action == "mark_spam" else (0.0 if "phishing" in email["body"].lower() else 0.5)
            },
            "categorization_accuracy": {
                "weight": 1.5,
                "evaluator": lambda action, email, idx, log: 1.0 if action == "categorize" and not email["is_critical"] else (0.0 if action == "categorize" and email["is_critical"] else 0.2)
            },
            "completion_rate": {
                "weight": 1.5,
                "evaluator": lambda action, email, idx, log: 1.0 if idx >= 5 else 0.6
            }
        }
    
    def _hard_criteria(self):
        """Complex criteria for hard task with multi-step reasoning."""
        def has_appropriate_followup(action, email, idx, log):
            if email["is_critical"] and action == "request_info":
                # Check if later action resolved it
                for later in log[idx:]:
                    if later["action"] == "escalate":
                        return 0.8
                return 0.3
            return 0.5
        
        def handles_conflicting_priority(action, email, idx, log):
            if email["is_urgent"] and email["is_critical"]:
                # Must prioritize correctly
                if action in ["prioritize_high", "escalate"]:
                    return 1.0
                return 0.0
            return 0.5
        
        return {
            "critical_workflow": {
                "weight": 3.0,
                "evaluator": has_appropriate_followup
            },
            "priority_accuracy": {
                "weight": 3.0,
                "evaluator": handles_conflicting_priority
            },
            "no_loops": {
                "weight": 2.0,
                "evaluator": lambda action, email, idx, log: 1.0 if not (action == "request_info" and idx > 0 and log[idx-1]["action"] == "request_info") else 0.0
            },
            "time_efficiency": {
                "weight": 1.0,
                "evaluator": lambda action, email, idx, log: 1.0 if idx < 7 else 0.4
            },
            "completeness": {
                "weight": 1.0,
                "evaluator": lambda action, email, idx, log: 1.0 if idx >= 7 else 0.5
            }
        }
    
    def _find_email_by_id(self, email_id: str, inbox: List[Dict]) -> Dict:
        for email in inbox:
            if email["id"] == email_id:
                return email
        return None
