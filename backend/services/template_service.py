import os
import json
import uuid
import time
from typing import List, Dict, Optional
from infra.logger import logger

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "templates")

class TemplateService:
    def __init__(self):
        if not os.path.exists(TEMPLATE_DIR):
            os.makedirs(TEMPLATE_DIR)

    def list_templates(self) -> List[Dict]:
        templates = []
        try:
            for filename in os.listdir(TEMPLATE_DIR):
                if filename.endswith(".json"):
                    filepath = os.path.join(TEMPLATE_DIR, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            templates.append(data)
                    except Exception as e:
                        logger.error(f"Failed to load template {filename}: {e}")
        except Exception as e:
            logger.error(f"Failed to list templates: {e}")
        
        # Sort by updated_at desc
        templates.sort(key=lambda x: x.get('updated_at', 0), reverse=True)
        return templates

    def get_template(self, template_id: str) -> Optional[Dict]:
        filepath = os.path.join(TEMPLATE_DIR, f"{template_id}.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to read template {template_id}: {e}")
        return None

    def create_template(self, name: str, tracks: Dict) -> Dict:
        template_id = str(uuid.uuid4())
        now = int(time.time() * 1000)
        template = {
            "id": template_id,
            "name": name,
            "created_at": now,
            "updated_at": now,
            "tracks": tracks
        }
        self._save_template(template)
        return template

    def update_template(self, template_id: str, data: Dict) -> Optional[Dict]:
        existing = self.get_template(template_id)
        if not existing:
            return None
        
        existing.update(data)
        existing['updated_at'] = int(time.time() * 1000)
        # Ensure ID doesn't change
        existing['id'] = template_id
        
        self._save_template(existing)
        return existing

    def delete_template(self, template_id: str) -> bool:
        filepath = os.path.join(TEMPLATE_DIR, f"{template_id}.json")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except Exception as e:
                logger.error(f"Failed to delete template {template_id}: {e}")
        return False

    def _save_template(self, template: Dict):
        filepath = os.path.join(TEMPLATE_DIR, f"{template['id']}.json")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(template, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save template {template['id']}: {e}")
            raise

template_service = TemplateService()
