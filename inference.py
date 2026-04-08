import os
import json
from openai import OpenAI
from environment import EmailTriageEnv

# Read API credentials from environment
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set")

# Initialize OpenAI client (works with HF inference endpoints)
client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key=HF_TOKEN
)

def run_baseline_inference(task_id: str, model: str = "meta-llama/Llama-3.2-3B-Instruct"):
    """Run baseline inference on a specific task."""
    env = EmailTriageEnv(task_id=task_id)
    obs = env.reset()
    done = False
    total_reward = 0.0
    steps = 0
    
    print(f"\n=== Running {task_id.upper()} task ===")
    print(f"Instruction: {obs.task_instruction}")
    
    while not done and steps < 50:
        # Prepare prompt for LLM
        prompt = f"""You are an email triage assistant. Current task: {obs.task_instruction}

Current email:
From: {obs.current_email['from_addr']}
Subject: {obs.current_email['subject']}
Body: {obs.current_email['body'][:200]}

Time remaining: {obs.time_remaining}

Choose one action from: archive, mark_spam, prioritize_high, prioritize_normal, prioritize_low, categorize, draft_reply, request_info, escalate

Action:"""
        
        try:
            # Call HF inference endpoint
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an email triage expert. Respond with only the action name."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=10
            )
            
            action = response.choices[0].message.content.strip().lower()
            
            # Validate action
            valid_actions = env.task_config["valid_actions"]
            if action not in valid_actions:
                print(f"  Invalid action: {action}, defaulting to archive")
                action = "archive"
            
            # Take step
            obs, reward, done, info = env.step(action)
            total_reward += reward.value
            steps += 1
            
            print(f"  Step {steps}: {action} -> reward: {reward.value:.2f}, remaining: {info['remaining_count']}")
            
        except Exception as e:
            print(f"  Error: {e}")
            break
    
    # Calculate final score
    final_score = env.calculate_final_reward()
    print(f"\nTask {task_id} completed: {steps} steps, cumulative reward: {total_reward:.2f}, final score: {final_score:.3f}")
    
    return {
        "task": task_id,
        "steps": steps,
        "cumulative_reward": total_reward,
        "final_score": final_score
    }

if __name__ == "__main__":
    results = []
    for task in ["easy", "medium", "hard"]:
        result = run_baseline_inference(task)
        results.append(result)
    
    print("\n=== SUMMARY ===")
    for r in results:
        print(f"{r['task']}: {r['final_score']:.3f}")
    
    # Save results
    with open("baseline_results.json", "w") as f:
        json.dump(results, f, indent=2)
