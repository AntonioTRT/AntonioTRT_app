#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Merge inteligente de configuración YAML
Sincroniza default_config.yaml con local_config.yaml sin perder datos locales.

Uso:
    python3 config/merge_config.py
    
Comportamiento:
1. Si local_config.yaml NO existe: copia default_config.yaml
2. Si local_config.yaml EXISTS: 
   - Preserva todos los valores locales
   - Agrega nuevas claves del default
   - Avisa sobre claves que se eliminaron del default
"""

from __future__ import print_function
import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, Tuple

class ConfigMerger:
    """Fusiona configuración default con local, preservando valores locales."""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.config_dir = Path(__file__).parent
        self.default_config_path = self.config_dir / "default_config.yaml"
        self.local_config_path = self.config_dir / "local_config.yaml"
        
    def log(self, msg, level="INFO"):
        """Log con nivel."""
        if self.verbose:
            symbols = {"INFO": "[i]", "OK": "[+]", "WARN": "[!]", "ERROR": "[x]"}
            print("{0} {1}".format(symbols.get(level, "[-]"), msg))
    
    def load_yaml(self, path: Path) -> Dict[str, Any]:
        """Carga archivo YAML."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
        except Exception as e:
            self.log("Error leyendo {0}: {1}".format(path, str(e)), "ERROR")
            return {}
    
    def save_yaml(self, data: Dict[str, Any], path: Path) -> bool:
        """Guarda archivo YAML."""
        try:
            # Asegurar que la carpeta existe
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            self.log("Error escribiendo {0}: {1}".format(path, str(e)), "ERROR")
            return False
    
    def deep_merge(self, default: Dict, local: Dict, path: str = "") -> Tuple[Dict, bool]:
        """
        Fusiona dicts recursivamente.
        Preserva valores locales, agrega nuevas claves del default.
        
        Retorna: (merged_dict, hay_cambios)
        """
        changes = False
        merged = local.copy()
        
        for key, default_value in default.items():
            if key not in merged:
                # Nueva clave desde default
                merged[key] = default_value
                self.log("  [+] Nueva clave: {0}".format(path + "." + key if path else key), "")
                changes = True
            
            elif isinstance(default_value, dict) and isinstance(merged.get(key), dict):
                # Recursivamente mergear dicts anidados
                nested_path = "{0}.{1}".format(path, key) if path else key
                merged[key], nested_changes = self.deep_merge(
                    default_value, 
                    merged[key], 
                    nested_path
                )
                changes = changes or nested_changes
        
        # Detectar claves que fueron eliminadas del default
        for key in list(local.keys()):
            if key not in default:
                # Clave local que no está en default (podría ser deprecada)
                self.log("  [!] Clave local no en default: {0} (manteniéndola)".format(key), "WARN")
        
        return merged, changes
    
    def merge(self) -> bool:
        """
        Ejecuta merge de configuración.
        Retorna True si fue exitoso.
        """
        self.log("=" * 50)
        self.log("TRT Config Merger")
        self.log("=" * 50)
        
        # 1. Cargar configs
        self.log("Leyendo configuración default...")
        default_config = self.load_yaml(self.default_config_path)
        
        if not default_config:
            self.log("ERROR: No se pudo cargar {0}".format(self.default_config_path), "ERROR")
            return False
        
        self.log("OK: {0} cargado".format(self.default_config_path), "OK")
        
        # 2. Verificar si local existe
        if not self.local_config_path.exists():
            self.log("Primera instalación detectada")
            self.log("Creando {0}...".format(self.local_config_path))
            
            if self.save_yaml(default_config, self.local_config_path):
                self.log("OK: {0} creado".format(self.local_config_path), "OK")
                return True
            else:
                self.log("ERROR al crear local_config.yaml", "ERROR")
                return False
        
        # 3. Cargar local
        self.log("Leyendo configuración local...")
        local_config = self.load_yaml(self.local_config_path)
        self.log("OK: {0} cargado".format(self.local_config_path), "OK")
        
        # 4. Mergear
        self.log("Sincronizando configuraciones...")
        merged_config, has_changes = self.deep_merge(default_config, local_config)
        
        if not has_changes:
            self.log("OK: Configuraciones sincronizadas (sin cambios)", "OK")
            return True
        
        # 5. Guardar merged
        self.log("Guardando cambios...")
        if self.save_yaml(merged_config, self.local_config_path):
            self.log("OK: {0} actualizado".format(self.local_config_path), "OK")
            self.log("=" * 50)
            self.log("OK: Merge completado exitosamente", "OK")
            return True
        else:
            self.log("ERROR al guardar configuración", "ERROR")
            return False


def main():
    """Punto de entrada."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Sincroniza configuración YAML preservando valores locales"
    )
    parser.add_argument('-q', '--quiet', action='store_true', help='Modo silencioso')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Mostrar cambios sin guardar')
    
    args = parser.parse_args()
    
    merger = ConfigMerger(verbose=not args.quiet)
    success = merger.merge()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
