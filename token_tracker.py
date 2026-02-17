import logging
from typing import Dict
from dataclasses import dataclass, field
from datetime import datetime

# Suppress token tracker logs in production
logging.getLogger(__name__).setLevel(logging.WARNING)

# Gemini API pricing (as of Feb 2026)
PRICING = {
    "gemini-2.5-flash-lite": {
        "input": 0.075 / 1_000_000,
        "output": 0.30 / 1_000_000
    },
    "gemini-2.0-flash": {
        "input": 0.10 / 1_000_000,
        "output": 0.40 / 1_000_000
    }
}

@dataclass
class TokenUsage:
    """Track token usage and costs"""
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def calculate_cost(self) -> float:
        """Calculate cost for this usage"""
        if self.model not in PRICING:
            return 0.0
        
        pricing = PRICING[self.model]
        input_cost = self.input_tokens * pricing["input"]
        output_cost = self.output_tokens * pricing["output"]
        return input_cost + output_cost

class TokenTracker:
    """Track token usage across all API calls"""
    
    def __init__(self, model: str = "gemini-2.5-flash-lite"):
        self.model = model
        self.usages = []
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.logger = logging.getLogger(__name__)
    
    def track(self, input_tokens: int, output_tokens: int) -> None:
        """Track token usage from API response"""
        usage = TokenUsage(
            model=self.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens
        )
        
        self.usages.append(usage)
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost += usage.calculate_cost()
    
    def get_summary(self) -> Dict:
        """Get usage summary"""
        return {
            "model": self.model,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": f"${self.total_cost:.6f}",
            "requests": len(self.usages),
            "avg_cost_per_request": f"${self.total_cost / len(self.usages):.6f}" if self.usages else "$0.00"
        }
    
    def print_summary(self) -> None:
        """Print usage summary to console"""
        summary = self.get_summary()
        print("\n" + "="*60)
        print("TOKEN USAGE SUMMARY")
        print("="*60)
        print(f"Model: {summary['model']}")
        print(f"Total Requests: {summary['requests']}")
        print(f"Input Tokens: {summary['total_input_tokens']:,}")
        print(f"Output Tokens: {summary['total_output_tokens']:,}")
        print(f"Total Tokens: {summary['total_tokens']:,}")
        print(f"Total Cost: {summary['total_cost']}")
        print(f"Avg Cost/Request: {summary['avg_cost_per_request']}")
        print("="*60 + "\n")

token_tracker = TokenTracker()
