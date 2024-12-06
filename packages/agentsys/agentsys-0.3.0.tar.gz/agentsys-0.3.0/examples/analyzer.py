from typing import Any, Dict, List
from ..core.agent import TaskAgent
from ..middleware.cache import cache_response
from ..middleware.retry import with_retry
from ..middleware.telemetry import with_telemetry
from ..protocols.streaming import StreamPipeline, StreamEvent, StreamType
from ..plugins.storage import FileStorage, StorageConfig
import asyncio
import json
from datetime import datetime
from pydantic import BaseModel

class DataPoint(BaseModel):
    """Represents a data point for analysis"""
    timestamp: datetime
    value: float
    metadata: Dict[str, Any] = {}

class AnalyzerAgent(TaskAgent):
    """An example agent that analyzes streaming data"""
    
    def __init__(self, name: str = "Analyzer", **kwargs):
        super().__init__(
            name=name,
            description="An agent that analyzes streaming data and identifies patterns",
            **kwargs
        )
        self.stream_pipeline = StreamPipeline[DataPoint]()
        self.storage = FileStorage(
            DataPoint,
            StorageConfig(storage_path="./data/analyzer")
        )
        self.analysis_results: List[Dict[str, Any]] = []
    
    async def initialize(self) -> None:
        """Initialize the analyzer"""
        await super().initialize()
        
        # Set up stream processing
        self.stream_pipeline.consumer.add_handler(
            StreamType.DATA,
            self._handle_data_point
        )
        
        # Start the pipeline
        await self.stream_pipeline.start()
    
    @cache_response(ttl=300)  # Cache for 5 minutes
    @with_retry(max_attempts=3)
    @with_telemetry("analyze_data")
    async def execute(self, input_data: Any) -> Any:
        """Analyze input data and generate insights"""
        # Convert input to DataPoint if needed
        if isinstance(input_data, dict):
            data_point = DataPoint(**input_data)
            await self.stream_pipeline.producer.send(data_point)
        
        # Perform analysis on accumulated data
        return await self._analyze_data()
    
    async def _handle_data_point(self, event: StreamEvent[DataPoint]) -> None:
        """Handle incoming data points"""
        if event.data:
            # Store data point
            await self.storage.put(
                f"data_point_{event.data.timestamp.isoformat()}",
                event.data
            )
            
            # Update analysis if needed
            if len(self.analysis_results) >= 100:
                self.analysis_results.pop(0)
            
            analysis = await self._analyze_single_point(event.data)
            self.analysis_results.append(analysis)
    
    async def _analyze_single_point(self, data_point: DataPoint) -> Dict[str, Any]:
        """Analyze a single data point"""
        # Example analysis
        return {
            "timestamp": data_point.timestamp,
            "value": data_point.value,
            "moving_average": await self._calculate_moving_average(data_point.value),
            "anomaly_score": await self._calculate_anomaly_score(data_point.value)
        }
    
    async def _calculate_moving_average(self, value: float, window: int = 10) -> float:
        """Calculate moving average"""
        values = [result["value"] for result in self.analysis_results[-window:]]
        values.append(value)
        return sum(values) / len(values)
    
    async def _calculate_anomaly_score(self, value: float) -> float:
        """Calculate anomaly score"""
        if not self.analysis_results:
            return 0.0
        
        # Simple z-score calculation
        values = [result["value"] for result in self.analysis_results]
        mean = sum(values) / len(values)
        std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
        
        if std == 0:
            return 0.0
        
        return abs(value - mean) / std
    
    async def _analyze_data(self) -> Dict[str, Any]:
        """Perform comprehensive analysis"""
        if not self.analysis_results:
            return {"status": "No data available"}
        
        # Calculate various metrics
        values = [result["value"] for result in self.analysis_results]
        anomaly_scores = [result["anomaly_score"] for result in self.analysis_results]
        
        return {
            "summary": {
                "count": len(values),
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "anomalies": sum(1 for score in anomaly_scores if score > 2.0)
            },
            "recent_trends": self.analysis_results[-10:],
            "timestamp": datetime.utcnow()
        }
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        await self.stream_pipeline.stop()
        await super().cleanup()

# Example usage
async def main():
    # Create and initialize analyzer
    analyzer = AnalyzerAgent()
    await analyzer.initialize()
    
    try:
        # Generate some sample data
        import random
        for i in range(20):
            data_point = DataPoint(
                timestamp=datetime.utcnow(),
                value=random.gauss(0, 1)
            )
            await analyzer.execute(data_point.dict())
            await asyncio.sleep(0.1)
        
        # Get final analysis
        analysis = await analyzer.execute(None)
        print("Final Analysis:", json.dumps(analysis, default=str, indent=2))
    
    finally:
        await analyzer.cleanup()

if __name__ == "__main__":
    asyncio.run(main())