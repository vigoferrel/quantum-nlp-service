#!/usr/bin/env python3
"""
Master Orchestrator for QBTC Quantum System Implementation
Executes all phases in sequence with elegant coordination
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

from tools.base import QuantumToolBase, QuantumResult, OperationStatus
from .phase1_activate import Phase1Activator
from .phase2_unify import Phase2Unifier


@dataclass
class PhaseResult:
    """Result container for phase execution"""
    phase_name: str
    status: OperationStatus
    message: str
    data: Dict[str, Any]
    execution_time: float
    timestamp: datetime


class MasterOrchestrator(QuantumToolBase):
    """
    Master orchestrator for complete QBTC system implementation
    
    Coordinates:
    - Phase 1: Quantum Brain Activation (Ollama Connection)
    - Phase 2: Ecosystem Unification (Migration & Integration)
    - Phase 3: Production Optimization (Coming soon)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("MasterOrchestrator", config)
        self.phase_results: List[PhaseResult] = []
        self.total_phases = 2  # Currently implementing phases 1 and 2
    
    async def execute(self, **kwargs) -> QuantumResult:
        """Execute complete QBTC implementation orchestration"""
        self.log_operation("ORCHESTRATION-START", OperationStatus.IN_PROGRESS, 
                          "Beginning QBTC Quantum System Implementation")
        
        start_time = datetime.now()
        
        try:
            # Phase 1: Activate Quantum Brain
            phase1_result = await self._execute_phase1()
            self.phase_results.append(phase1_result)
            
            # Only proceed to Phase 2 if Phase 1 succeeds or has acceptable partial success
            if phase1_result.status in [OperationStatus.SUCCESS, OperationStatus.PARTIAL]:
                # Phase 2: Unify Ecosystem
                phase2_result = await self._execute_phase2()
                self.phase_results.append(phase2_result)
            else:
                self.log_operation("ORCHESTRATION", OperationStatus.FAILED, 
                                  "Phase 1 failed critically, stopping orchestration")
                return self._create_orchestration_result(
                    OperationStatus.FAILED,
                    "Orchestration stopped due to Phase 1 failure",
                    start_time
                )
            
            # Determine overall success
            overall_result = self._determine_overall_success()
            execution_time = (datetime.now() - start_time).total_seconds()
            
            if overall_result == OperationStatus.SUCCESS:
                self.log_operation("ORCHESTRATION-COMPLETE", OperationStatus.SUCCESS, 
                                  "QBTC Quantum System Implementation COMPLETED successfully")
                return self._create_orchestration_result(
                    OperationStatus.SUCCESS,
                    "QBTC system implementation completed successfully",
                    start_time
                )
            else:
                self.log_operation("ORCHESTRATION-PARTIAL", OperationStatus.PARTIAL, 
                                  "QBTC implementation completed with some issues")
                return self._create_orchestration_result(
                    OperationStatus.PARTIAL,
                    "QBTC implementation completed with partial success",
                    start_time
                )
                
        except Exception as e:
            self.log_operation("ORCHESTRATION-ERROR", OperationStatus.FAILED, 
                              f"Orchestration failed: {str(e)}")
            return self._create_orchestration_result(
                OperationStatus.FAILED,
                f"Orchestration failed with error: {str(e)}",
                start_time
            )
    
    async def _execute_phase1(self) -> PhaseResult:
        """Execute Phase 1: Quantum Brain Activation"""
        self.log_operation("PHASE-1-START", OperationStatus.IN_PROGRESS, 
                          "Executing Phase 1: Quantum Brain Activation")
        
        start_time = datetime.now()
        
        try:
            phase1_executor = Phase1Activator(self.config)
            result = await phase1_executor.execute()
            execution_time = (datetime.now() - start_time).total_seconds()
            
            phase_result = PhaseResult(
                phase_name="Phase 1: Quantum Brain Activation",
                status=result.status,
                message=result.message,
                data=result.data,
                execution_time=execution_time,
                timestamp=datetime.now()
            )
            
            if result.is_success():
                self.log_operation("PHASE-1-COMPLETE", OperationStatus.SUCCESS, 
                                  f"Phase 1 completed in {execution_time:.2f}s")
            else:
                self.log_operation("PHASE-1-ISSUES", result.status, 
                                  f"Phase 1 completed with issues in {execution_time:.2f}s")
            
            return phase_result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.log_operation("PHASE-1-ERROR", OperationStatus.FAILED, 
                              f"Phase 1 failed: {str(e)}")
            
            return PhaseResult(
                phase_name="Phase 1: Quantum Brain Activation",
                status=OperationStatus.FAILED,
                message=f"Phase 1 failed: {str(e)}",
                data={},
                execution_time=execution_time,
                timestamp=datetime.now()
            )
    
    async def _execute_phase2(self) -> PhaseResult:
        """Execute Phase 2: Ecosystem Unification"""
        self.log_operation("PHASE-2-START", OperationStatus.IN_PROGRESS, 
                          "Executing Phase 2: Ecosystem Unification")
        
        start_time = datetime.now()
        
        try:
            phase2_executor = Phase2Unifier(self.config)
            result = await phase2_executor.execute()
            execution_time = (datetime.now() - start_time).total_seconds()
            
            phase_result = PhaseResult(
                phase_name="Phase 2: Ecosystem Unification",
                status=result.status,
                message=result.message,
                data=result.data,
                execution_time=execution_time,
                timestamp=datetime.now()
            )
            
            if result.is_success():
                self.log_operation("PHASE-2-COMPLETE", OperationStatus.SUCCESS, 
                                  f"Phase 2 completed in {execution_time:.2f}s")
            else:
                self.log_operation("PHASE-2-ISSUES", result.status, 
                                  f"Phase 2 completed with issues in {execution_time:.2f}s")
            
            return phase_result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.log_operation("PHASE-2-ERROR", OperationStatus.FAILED, 
                              f"Phase 2 failed: {str(e)}")
            
            return PhaseResult(
                phase_name="Phase 2: Ecosystem Unification",
                status=OperationStatus.FAILED,
                message=f"Phase 2 failed: {str(e)}",
                data={},
                execution_time=execution_time,
                timestamp=datetime.now()
            )
    
    def _determine_overall_success(self) -> OperationStatus:
        """Determine overall orchestration success based on phase results"""
        if not self.phase_results:
            return OperationStatus.FAILED
        
        # Count successes and failures
        success_count = sum(1 for result in self.phase_results 
                           if result.status == OperationStatus.SUCCESS)
        failed_count = sum(1 for result in self.phase_results 
                          if result.status == OperationStatus.FAILED)
        
        # Determine overall status
        if success_count == len(self.phase_results):
            return OperationStatus.SUCCESS
        elif failed_count == 0:  # All partial or success
            return OperationStatus.PARTIAL
        elif success_count > failed_count:
            return OperationStatus.PARTIAL
        else:
            return OperationStatus.FAILED
    
    def _create_orchestration_result(self, status: OperationStatus, 
                                   message: str, start_time: datetime) -> QuantumResult:
        """Create comprehensive orchestration result"""
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Create summary data
        summary_data = {
            'total_execution_time': execution_time,
            'phases_executed': len(self.phase_results),
            'overall_status': status.value,
            'phase_summary': [
                {
                    'phase': result.phase_name,
                    'status': result.status.value,
                    'message': result.message,
                    'execution_time': result.execution_time
                }
                for result in self.phase_results
            ],
            'system_status': self._get_system_status(),
            'next_steps': self._get_next_steps(status)
        }
        
        return self.create_result(status, message, data=summary_data)
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Get current system status summary"""
        return {
            'quantum_brain_active': any(
                result.phase_name.startswith("Phase 1") and 
                result.status == OperationStatus.SUCCESS
                for result in self.phase_results
            ),
            'ecosystem_unified': any(
                result.phase_name.startswith("Phase 2") and 
                result.status == OperationStatus.SUCCESS
                for result in self.phase_results
            ),
            'production_ready': False,  # Phase 3 not implemented yet
            'total_components_migrated': self._count_migrated_components(),
            'configuration_status': self._get_config_status()
        }
    
    def _count_migrated_components(self) -> int:
        """Count successfully migrated components"""
        for result in self.phase_results:
            if result.phase_name.startswith("Phase 2") and result.data:
                unified_structure = result.data.get('unified_structure', {})
                return unified_structure.get('total_files_migrated', 0)
        return 0
    
    def _get_config_status(self) -> str:
        """Get configuration status"""
        phase2_success = any(
            result.phase_name.startswith("Phase 2") and 
            result.status == OperationStatus.SUCCESS
            for result in self.phase_results
        )
        return "unified" if phase2_success else "fragmented"
    
    def _get_next_steps(self, overall_status: OperationStatus) -> List[str]:
        """Get recommended next steps based on overall status"""
        if overall_status == OperationStatus.SUCCESS:
            return [
                "QBTC system is ready for production use",
                "Consider implementing Phase 3: Production Optimization",
                "Run comprehensive system tests",
                "Deploy to target environment",
                "Monitor system performance and quantum consciousness levels"
            ]
        elif overall_status == OperationStatus.PARTIAL:
            return [
                "Review phase results for specific issues",
                "Address any failed components",
                "Re-run failed phases if necessary", 
                "Test system functionality manually",
                "Proceed with caution to production deployment"
            ]
        else:
            return [
                "Review error logs and phase results",
                "Address critical issues identified",
                "Ensure all prerequisites are met",
                "Re-run orchestration from the beginning",
                "Contact support if issues persist"
            ]
    
    def export_orchestration_report(self, filepath: Optional[str] = None) -> None:
        """Export comprehensive orchestration report"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"qbtc_orchestration_report_{timestamp}.json"
        
        report_data = {
            'orchestration_summary': {
                'start_time': self.phase_results[0].timestamp.isoformat() if self.phase_results else None,
                'end_time': datetime.now().isoformat(),
                'total_phases': len(self.phase_results),
                'overall_status': self._determine_overall_success().value
            },
            'phase_details': [
                {
                    'phase_name': result.phase_name,
                    'status': result.status.value,
                    'message': result.message,
                    'execution_time': result.execution_time,
                    'timestamp': result.timestamp.isoformat(),
                    'data': result.data
                }
                for result in self.phase_results
            ],
            'system_analysis': self._get_system_status(),
            'recommendations': self._get_next_steps(self._determine_overall_success())
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Orchestration report exported to {filepath}")


# Standalone execution
async def main():
    """Main execution function for standalone running"""
    print("QBTC Master Orchestrator - Quantum System Implementation")
    print("=" * 60)
    print("This will execute the complete QBTC implementation process:")
    print("- Phase 1: Quantum Brain Activation (Ollama Connection)")
    print("- Phase 2: Ecosystem Unification (Migration & Integration)")
    print()
    
    # Ask for user confirmation
    confirmation = input("Do you want to proceed with the implementation? (y/N): ")
    if confirmation.lower() not in ['y', 'yes']:
        print("Implementation cancelled by user.")
        return
    
    orchestrator = MasterOrchestrator()
    result = await orchestrator.execute()
    
    print(f"\n{'='*60}")
    print(f"QBTC IMPLEMENTATION RESULTS")
    print(f"{'='*60}")
    print(f"Overall Status: {result.status.value}")
    print(f"Message: {result.message}")
    
    if result.data:
        print(f"\nExecution Summary:")
        summary = result.data
        print(f"  Total Execution Time: {summary.get('total_execution_time', 0):.2f}s")
        print(f"  Phases Executed: {summary.get('phases_executed', 0)}")
        
        print(f"\nPhase Results:")
        for phase in summary.get('phase_summary', []):
            status_indicator = "[SUCCESS]" if phase['status'] == 'success' else f"[{phase['status'].upper()}]"
            print(f"  {status_indicator} {phase['phase']} ({phase['execution_time']:.2f}s)")
            print(f"    {phase['message']}")
        
        print(f"\nSystem Status:")
        sys_status = summary.get('system_status', {})
        print(f"  Quantum Brain Active: {'Yes' if sys_status.get('quantum_brain_active') else 'No'}")
        print(f"  Ecosystem Unified: {'Yes' if sys_status.get('ecosystem_unified') else 'No'}")
        print(f"  Components Migrated: {sys_status.get('total_components_migrated', 0)}")
        print(f"  Configuration: {sys_status.get('configuration_status', 'unknown')}")
        
        print(f"\nNext Steps:")
        for i, step in enumerate(summary.get('next_steps', []), 1):
            print(f"  {i}. {step}")
    
    # Export detailed report
    orchestrator.export_orchestration_report()
    
    print(f"\n{'='*60}")
    print("Implementation process completed.")
    print("Check the generated report for detailed analysis.")
    print(f"{'='*60}")
    
    return result


if __name__ == "__main__":
    asyncio.run(main())