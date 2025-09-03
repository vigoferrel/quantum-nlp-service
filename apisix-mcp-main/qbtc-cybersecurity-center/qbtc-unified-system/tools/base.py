#!/usr/bin/env python3
"""
Base class for QBTC Quantum Tools
Provides elegant foundation for all quantum operations
"""

import logging
import json
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union
from enum import Enum

import colorama
from colorama import Fore, Style


class OperationStatus(Enum):
    """Status of quantum operations"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class QuantumResult:
    """Elegant result container for quantum operations"""
    status: OperationStatus
    message: str
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def is_success(self) -> bool:
        """Check if operation was successful"""
        return self.status == OperationStatus.SUCCESS
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'status': self.status.value,
            'message': self.message,
            'data': self.data,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        }


class QuantumToolBase(ABC):
    """
    Elegant base class for all QBTC quantum tools
    
    Provides:
    - Structured logging with colors
    - Configuration management
    - Error handling patterns
    - Result standardization
    - Progress tracking
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = self._setup_logger()
        self.results: Dict[str, QuantumResult] = {}
        
        # Initialize colorama for Windows
        colorama.init(autoreset=True)
        
        self.logger.info(f"{Fore.CYAN}Quantum Tool {self.name} initialized{Style.RESET_ALL}")
    
    def _setup_logger(self) -> logging.Logger:
        """Setup elegant structured logging"""
        logger = logging.getLogger(f"quantum.{self.name}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'{Fore.BLUE}%(asctime)s{Style.RESET_ALL} - '
                f'{Fore.MAGENTA}[%(name)s]{Style.RESET_ALL} - '
                f'%(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def log_operation(self, operation: str, status: OperationStatus, 
                     message: str, **kwargs) -> None:
        """Log operation with elegant formatting"""
        status_colors = {
            OperationStatus.PENDING: Fore.YELLOW,
            OperationStatus.IN_PROGRESS: Fore.BLUE,
            OperationStatus.SUCCESS: Fore.GREEN,
            OperationStatus.FAILED: Fore.RED,
            OperationStatus.PARTIAL: Fore.YELLOW
        }
        
        color = status_colors.get(status, Fore.WHITE)
        status_symbol = {
            OperationStatus.PENDING: "[PENDING]",
            OperationStatus.IN_PROGRESS: "[IN_PROGRESS]",
            OperationStatus.SUCCESS: "[SUCCESS]",
            OperationStatus.FAILED: "[FAILED]",
            OperationStatus.PARTIAL: "[PARTIAL]"
        }.get(status, "[INFO]")
        
        log_message = f"{status_symbol} {color}{operation}: {message}{Style.RESET_ALL}"
        
        if status == OperationStatus.FAILED:
            self.logger.error(log_message)
        elif status == OperationStatus.SUCCESS:
            self.logger.info(log_message)
        else:
            self.logger.info(log_message)
    
    def create_result(self, status: OperationStatus, message: str, 
                     **kwargs) -> QuantumResult:
        """Create standardized quantum result"""
        return QuantumResult(status=status, message=message, **kwargs)
    
    def save_result(self, operation_id: str, result: QuantumResult) -> None:
        """Save operation result for tracking"""
        self.results[operation_id] = result
        self.log_operation(f"Result-{operation_id}", result.status, result.message)
    
    @abstractmethod
    async def execute(self, **kwargs) -> QuantumResult:
        """Execute the quantum operation - must be implemented by subclasses"""
        pass
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value with fallback"""
        return self.config.get(key, default)
    
    async def verify_prerequisites(self) -> QuantumResult:
        """Verify tool prerequisites - can be overridden"""
        return self.create_result(
            OperationStatus.SUCCESS,
            "Prerequisites verification passed"
        )
    
    def export_results(self, filepath: Optional[Union[str, Path]] = None) -> None:
        """Export all results to JSON file"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"quantum_results_{self.name}_{timestamp}.json"
        
        results_dict = {
            op_id: result.to_dict() 
            for op_id, result in self.results.items()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results exported to {filepath}")


class QuantumPhaseExecutor(QuantumToolBase):
    """Base class for quantum phase executors"""
    
    def __init__(self, phase_name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(f"Phase-{phase_name}", config)
        self.phase_name = phase_name
        self.steps_completed = 0
        self.total_steps = 0
    
    def set_total_steps(self, total: int) -> None:
        """Set total number of steps for progress tracking"""
        self.total_steps = total
        self.logger.info(f"Phase {self.phase_name} has {total} steps")
    
    def complete_step(self, step_name: str) -> None:
        """Mark a step as completed"""
        self.steps_completed += 1
        progress = (self.steps_completed / self.total_steps * 100) if self.total_steps > 0 else 0
        
        self.log_operation(
            f"Step-{self.steps_completed}",
            OperationStatus.SUCCESS,
            f"{step_name} ({progress:.1f}% complete)"
        )
    
    def get_progress(self) -> float:
        """Get current progress percentage"""
        return (self.steps_completed / self.total_steps * 100) if self.total_steps > 0 else 0