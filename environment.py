import json
import random
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from openenv import OpenEnv, Observation, Action, Reward
from tasks import EMAIL_TASKS
from graders import EmailTriageGrader

class Email(BaseModel):
    id: str
    from_addr: str
    subject: str
    body: str
    received_at: str
    is_urgent: bool = False
    is_critical: bool = False

class InboxState(BaseModel):
    emails: List[Email]
    current_index: int
    triage_log: List[Dict]
    time_remaining: int

class EmailTriageEnv(OpenEnv):
    """Real-world email triage environment for knowledge workers."""
    
    def __init__(self, task_id: str = "easy"):
        super().__init__()
        self.task_id = task_id
        self.task_config = EMAIL_TASKS[task_id]
        self.grader = EmailTriageGrader(task_id)
        self.state = None
        self.reset()
    
    def reset(self) -> Observation:
        """Reset environment to initial state."""
        initial_inbox = self.task_config["initial_inbox"]
        self.state = InboxState(
            emails=[Email(**email) for email in initial_inbox],
            current_index=0,
            triage_log=[],
            time_remaining=self.task_config["time_limit"]
        )
        
        return Observation(
            inbox=[email.dict() for email in self.state.emails],
            current_email=self.state.emails[0].dict() if self.state.emails else None,
            time_remaining=self.state.time_remaining,
            task_instruction=self.task_config["instruction"]
        )
    
    def step(self, action: Action) -> tuple[Observation, Reward, bool, Dict]:
        """Execute one step in the environment."""
        action_value = action.value
        
        # Validate action
        if action_value not in self.task_config["valid_actions"]:
            reward = Reward(value=-0.2, reason=f"Invalid action: {action_value}")
            done = False
            info = {"error": "invalid_action"}
            return self._get_observation(), reward, done, info
        
        # Process action
        current_email = self.state.emails[self.state.current_index] if self.state.emails else None
        
        if not current_email:
            return self._get_observation(), Reward(value=0.0, reason="No emails left"), True, {"completed": True}
        
        # Log action
        self.state.triage_log.append({
            "email_id": current_email.id,
            "action": action_value,
            "timestamp": datetime.now().isoformat()
        })
        
        # Calculate incremental reward
        reward_value = self._calculate_incremental_reward(action_value, current_email)
        
        # Update state
        if action_value in ["archive", "mark_spam"]:
            # Remove email from inbox
            self.state.emails.pop(self.state.current_index)
            # Don't increment index since next email shifts into position
        else:
            # Move to next email
            self.state.current_index += 1
        
        # Check for completion
        done = self.state.current_index >= len(self.state.emails) or self.state.time_remaining <= 0
        
        # Decrease time
        self.state.time_remaining -= 1
        
        info = {
            "triaged_count": len(self.state.triage_log),
            "remaining_count": len(self.state.emails) - self.state.current_index
        }
        
        return self._get_observation(), Reward(value=reward_value, reason=f"Action: {action_value}"), done, info
    
    def _calculate_incremental_reward(self, action: str, email: Email) -> float:
        """Calculate reward based on action appropriateness."""
        # Penalize destructive or loop actions
        if action == "request_info" and len(self.state.triage_log) > 3:
            # Penalize repeated request_info without progress
            recent_requests = sum(1 for log in self.state.triage_log[-3:] if log["action"] == "request_info")
            if recent_requests >= 2:
                return -0.15
        
        # Base reward for taking any action
        base_reward = 0.1
        
        # Priority appropriateness
        if email.is_critical and action == "escalate":
            return base_reward + 0.5
        elif email.is_critical and action in ["archive", "mark_spam"]:
            return -0.5
        elif email.is_urgent and action in ["prioritize_high", "draft_reply"]:
            return base_reward + 0.3
        elif email.is_urgent and action == "prioritize_low":
            return -0.3
        
        # Spam detection
        if "spam" in email.body.lower() or "lottery" in email.body.lower():
            if action == "mark_spam":
                return base_reward + 0.4
            else:
                return -0.2
        
        # Normal email handling
        if action == "archive":
            return base_reward + 0.2
        elif action == "categorize":
            return base_reward + 0.15
        
        return base_reward
    
    def _get_observation(self) -> Observation:
        """Get current observation."""
        current = self.state.emails[self.state.current_index] if self.state.current_index < len(self.state.emails) else None
        return Observation(
            inbox=[email.dict() for email in self.state.emails[self.state.current_index:]],
            current_email=current.dict() if current else None,
            time_remaining=self.state.time_remaining,
            task_instruction=self.task_config["instruction"]
        )
    
    def state(self) -> Dict[str, Any]:
        """Return current internal state for debugging."""
        return {
            "task_id": self.task_id,
            "current_index": self.state.current_index,
            "triage_log": self.state.triage_log,
            "time_remaining": self.state.time_remaining,
            "emails_remaining": len(self.state.emails) - self.state.current_index
        }

    def calculate_final_reward(self) -> float:
        """Calculate final score using programmatic grader."""
        return self.grader.grade(self.state.triage_log, self.task_config)
