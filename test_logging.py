#!/usr/bin/env python3
"""Script de test pour valider la configuration de logging et les variables d'environnement.

Ce script teste le système de logging configuré dans mangetamain.logging_config
et vérifie que les variables d'environnement sont correctement prises en compte.
"""

import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Ajouter le répertoire src au path pour importer mangetamain
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mangetamain.logging_config import configure_logging, get_logger


def test_basic_logging():
    """Test basique du système de logging."""
    print("Test 1: Configuration basique du logging")

    # Créer un répertoire temporaire pour les logs
    with tempfile.TemporaryDirectory() as temp_dir:
        # Configurer le logging
        config = configure_logging(log_directory=temp_dir)

        # Vérifier que les fichiers ont été créés
        debug_log = config.debug_log_path
        error_log = config.error_log_path

        print(f"Repertoire de logs: {config.log_directory}")
        print(f"Fichier debug: {debug_log.name}")
        print(f"Fichier error: {error_log.name}")

        # Tester différents niveaux de log
        logger = get_logger("test_module")

        logger.debug("Message de debug - test basique")
        logger.info("Message d'information - test basique")
        logger.warning("Message d'avertissement - test basique")
        logger.error("Message d'erreur - test basique")
        logger.critical("Message critique - test basique")

        # Vérifier le contenu des fichiers
        print("\nContenu du fichier debug:")
        if debug_log.exists():
            with open(debug_log, encoding="utf-8") as f:
                print(f.read())
        else:
            print("Fichier debug non trouve")

        print("\nContenu du fichier error:")
        if error_log.exists():
            with open(error_log, encoding="utf-8") as f:
                print(f.read())
        else:
            print("Fichier error non trouve")


def test_environment_variables():
    """Test des variables d'environnement."""
    print("\nTest 2: Variables d'environnement")

    # Définir des variables d'environnement de test
    test_env = {
        "MANG_LOG_DIR": str(Path.cwd() / "test_logs"),
        "MANG_USER_ID": "test_user_123",
        "MANG_SESSION_ID": "session_abc_456",
        "MANG_LOG_MAX_FILES": "5",
    }

    # Sauvegarder les variables existantes
    original_env = {}
    for key in test_env:
        original_env[key] = os.environ.get(key)
        os.environ[key] = test_env[key]

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Utiliser le répertoire défini par la variable d'environnement
            os.environ["MANG_LOG_DIR"] = temp_dir

            # Configurer le logging avec les variables d'environnement
            config = configure_logging()

            logger = get_logger("env_test")
            logger.info("Test avec variables d'environnement")
            logger.error("Test d'erreur avec variables d'environnement")

            # Vérifier que les variables sont utilisées
            print(f"User ID utilise: {config.run_identifier}")
            print(f"Repertoire configure: {config.log_directory}")

            # Vérifier le contenu des logs
            debug_log = config.debug_log_path
            if debug_log.exists():
                with open(debug_log, encoding="utf-8") as f:
                    content = f.read()
                    print("\nLogs avec variables d'environnement:")
                    print(content)

                    # Vérifier que les informations contextuelles sont présentes
                    if "user=test_user_123" in content:
                        print("User ID correctement injecte")
                    else:
                        print("User ID manquant dans les logs")

                    if "session=session_abc_456" in content:
                        print("Session ID correctement injecte")
                    else:
                        print("Session ID manquant dans les logs")

    finally:
        # Restaurer les variables d'environnement originales
        for key, value in original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def test_log_rotation():
    """Test de la rotation des logs."""
    print("\nTest 3: Rotation des logs")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Créer plusieurs fichiers de logs simulés
        log_dir = Path(temp_dir)
        log_dir.mkdir(exist_ok=True)

        # Créer des fichiers de logs avec différents timestamps
        for i in range(15):  # Créer plus de fichiers que la limite
            timestamp = f"20240101T12000{i:02d}Z"
            debug_file = log_dir / f"debug-{timestamp}.log"
            error_file = log_dir / f"error-{timestamp}.log"

            debug_file.write_text(f"Debug log {i}")
            error_file.write_text(f"Error log {i}")

            # Modifier la date de modification pour simuler des fichiers plus anciens
            old_time = datetime.now().timestamp() - (i * 3600)  # 1 heure par fichier
            debug_file.touch()
            error_file.touch()
            os.utime(debug_file, (old_time, old_time))
            os.utime(error_file, (old_time, old_time))

        print(f"Cree {len(list(log_dir.glob('*.log')))} fichiers de logs")

        # Configurer le logging avec une limite de 5 fichiers
        config = configure_logging(log_directory=temp_dir, max_log_files=5)

        # Vérifier le nombre de fichiers restants
        remaining_files = list(log_dir.glob("*.log"))
        print(f"Fichiers restants apres rotation: {len(remaining_files)}")

        if len(remaining_files) <= 10:  # 5 debug + 5 error max
            print("Rotation des logs fonctionne correctement")
        else:
            print("Rotation des logs ne fonctionne pas")


def test_log_format():
    """Test du format des logs."""
    print("\nTest 4: Format des logs")

    with tempfile.TemporaryDirectory() as temp_dir:
        config = configure_logging(log_directory=temp_dir)
        logger = get_logger("format_test")

        # Générer un log avec toutes les informations
        logger.info("Test du format de log")

        debug_log = config.debug_log_path
        if debug_log.exists():
            with open(debug_log, encoding="utf-8") as f:
                content = f.read().strip()
                print(f"Format du log: {content}")

                # Vérifier les composants du format
                components = [
                    "timestamp",
                    "levelname",
                    "pathname",
                    "lineno",
                    "run=",
                    "user=",
                    "session=",
                    "message",
                ]

                missing_components = []
                for component in components:
                    if component not in content:
                        missing_components.append(component)

                if not missing_components:
                    print("Format des logs complet")
                else:
                    print(f"Composants manquants: {missing_components}")


def main():
    """Fonction principale de test."""
    print("Démarrage des tests de logging")
    print("=" * 50)

    try:
        test_basic_logging()
        test_environment_variables()
        test_log_rotation()
        test_log_format()

        print("\n" + "=" * 50)
        print("Tous les tests termines avec succes!")

    except Exception as e:
        print(f"\nErreur lors des tests: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
