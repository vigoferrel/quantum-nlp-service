"""
Supabase storage integration for LLM model artifacts and metadata.
Handles storage and retrieval of model weights, checkpoints, and associated metadata.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Union
from supabase import create_client, Client

class SupabaseArtifactStorage:
    def __init__(self, supabase_url: str, supabase_key: str):
        """Initialize Supabase client and storage buckets."""
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self._ensure_storage_buckets()
    
    def _ensure_storage_buckets(self):
        """Ensure required storage buckets exist."""
        required_buckets = ['model-weights', 'checkpoints', 'config', 'metadata']
        for bucket in required_buckets:
            try:
                self.supabase.storage.get_bucket(bucket)
            except:
                self.supabase.storage.create_bucket(bucket)

    def store_model_weights(self, model_id: str, weights_path: str, metadata: Dict) -> str:
        """Store model weights and associated metadata."""
        # Upload weights file
        with open(weights_path, 'rb') as f:
            self.supabase.storage.from_('model-weights').upload(
                f"{model_id}/weights.pt",
                f
            )

        # Store metadata
        metadata.update({
            'model_id': model_id,
            'uploaded_at': datetime.utcnow().isoformat(),
            'file_path': f"model-weights/{model_id}/weights.pt"
        })
        
        self.supabase.table('model_artifacts').insert(metadata).execute()
        
        return model_id

    def store_checkpoint(self, model_id: str, checkpoint_path: str, 
                        metadata: Dict, checkpoint_name: Optional[str] = None) -> str:
        """Store training checkpoint and metadata."""
        if not checkpoint_name:
            checkpoint_name = f"checkpoint_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        # Upload checkpoint file
        with open(checkpoint_path, 'rb') as f:
            self.supabase.storage.from_('checkpoints').upload(
                f"{model_id}/{checkpoint_name}.pt",
                f
            )

        # Store metadata
        metadata.update({
            'model_id': model_id,
            'checkpoint_name': checkpoint_name,
            'uploaded_at': datetime.utcnow().isoformat(),
            'file_path': f"checkpoints/{model_id}/{checkpoint_name}.pt"
        })
        
        self.supabase.table('model_checkpoints').insert(metadata).execute()
        
        return checkpoint_name

    def store_config(self, model_id: str, config: Union[Dict, str], config_name: str) -> str:
        """Store model configuration."""
        if isinstance(config, dict):
            config_data = json.dumps(config)
        else:
            config_data = config

        # Upload config file
        self.supabase.storage.from_('config').upload(
            f"{model_id}/{config_name}.json",
            config_data
        )

        # Store metadata
        metadata = {
            'model_id': model_id,
            'config_name': config_name,
            'uploaded_at': datetime.utcnow().isoformat(),
            'file_path': f"config/{model_id}/{config_name}.json"
        }
        
        self.supabase.table('model_configs').insert(metadata).execute()
        
        return config_name

    def store_training_logs(self, model_id: str, logs: Union[Dict, List, str], 
                          log_name: Optional[str] = None) -> str:
        """Store training logs and metadata."""
        if not log_name:
            log_name = f"training_log_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        if isinstance(logs, (dict, list)):
            log_data = json.dumps(logs)
        else:
            log_data = logs

        # Upload log file
        self.supabase.storage.from_('metadata').upload(
            f"{model_id}/{log_name}.json",
            log_data
        )

        # Store metadata
        metadata = {
            'model_id': model_id,
            'log_name': log_name,
            'uploaded_at': datetime.utcnow().isoformat(),
            'file_path': f"metadata/{model_id}/{log_name}.json"
        }
        
        self.supabase.table('training_logs').insert(metadata).execute()
        
        return log_name

    def get_model_weights(self, model_id: str, local_path: str) -> str:
        """Retrieve model weights to local path."""
        try:
            self.supabase.storage.from_('model-weights').download(
                f"{model_id}/weights.pt",
                local_path
            )
            return local_path
        except Exception as e:
            raise Exception(f"Failed to retrieve model weights: {str(e)}")

    def get_checkpoint(self, model_id: str, checkpoint_name: str, local_path: str) -> str:
        """Retrieve checkpoint to local path."""
        try:
            self.supabase.storage.from_('checkpoints').download(
                f"{model_id}/{checkpoint_name}.pt",
                local_path
            )
            return local_path
        except Exception as e:
            raise Exception(f"Failed to retrieve checkpoint: {str(e)}")

    def get_config(self, model_id: str, config_name: str) -> Dict:
        """Retrieve model configuration."""
        try:
            data = self.supabase.storage.from_('config').download(
                f"{model_id}/{config_name}.json"
            )
            return json.loads(data)
        except Exception as e:
            raise Exception(f"Failed to retrieve config: {str(e)}")

    def get_training_logs(self, model_id: str, log_name: str) -> Union[Dict, List]:
        """Retrieve training logs."""
        try:
            data = self.supabase.storage.from_('metadata').download(
                f"{model_id}/{log_name}.json"
            )
            return json.loads(data)
        except Exception as e:
            raise Exception(f"Failed to retrieve training logs: {str(e)}")

    def list_model_artifacts(self, model_id: str) -> Dict[str, List]:
        """List all artifacts associated with a model."""
        return {
            'weights': self.supabase.storage.from_('model-weights').list(f"{model_id}/"),
            'checkpoints': self.supabase.storage.from_('checkpoints').list(f"{model_id}/"),
            'configs': self.supabase.storage.from_('config').list(f"{model_id}/"),
            'logs': self.supabase.storage.from_('metadata').list(f"{model_id}/")
        }

    def get_artifact_metadata(self, model_id: str) -> Dict[str, List]:
        """Get metadata for all artifacts of a model."""
        return {
            'model': self.supabase.table('model_artifacts')
                .select('*')
                .eq('model_id', model_id)
                .execute(),
            'checkpoints': self.supabase.table('model_checkpoints')
                .select('*')
                .eq('model_id', model_id)
                .execute(),
            'configs': self.supabase.table('model_configs')
                .select('*')
                .eq('model_id', model_id)
                .execute(),
            'logs': self.supabase.table('training_logs')
                .select('*')
                .eq('model_id', model_id)
                .execute()
        }
