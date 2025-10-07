#!/usr/bin/env python3
"""Script pour tester spécifiquement les variables d'environnement du système de logging.

Ce script démontre comment configurer et utiliser les variables d'environnement
pour personnaliser le comportement du système de logging.
"""

import os
import sys
import tempfile
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mangetamain.logging_config import configure_logging, get_logger


def demonstrate_environment_variables():
    """Démontre l'utilisation des variables d'environnement."""
    print("Variables d'environnement supportees:")
    print("=" * 50)

    env_vars = {
        "MANG_LOG_DIR": "Répertoire où stocker les fichiers de logs",
        "MANG_USER_ID": "Identifiant de l'utilisateur pour le contexte",
        "MANG_SESSION_ID": "Identifiant de session pour le contexte",
        "MANG_LOG_MAX_FILES": "Nombre maximum de fichiers de logs à conserver",
    }

    for var, description in env_vars.items():
        current_value = os.environ.get(var, "Non définie")
        print(f"{var}: {current_value}")
        print(f"   {description}")
        print()

    print("Pour definir ces variables en PowerShell:")
    print("   $env:MANG_LOG_DIR = 'C:\\logs'")
    print("   $env:MANG_USER_ID = 'mon_utilisateur'")
    print("   $env:MANG_SESSION_ID = 'session_123'")
    print("   $env:MANG_LOG_MAX_FILES = '20'")
    print()

    print("Pour definir ces variables en CMD:")
    print("   set MANG_LOG_DIR=C:\\logs")
    print("   set MANG_USER_ID=mon_utilisateur")
    print("   set MANG_SESSION_ID=session_123")
    print("   set MANG_LOG_MAX_FILES=20")
    print()


def test_custom_log_directory():
    """Test avec un répertoire de logs personnalisé."""
    print("Test: Repertoire de logs personnalise")

    # Créer un répertoire temporaire
    with tempfile.TemporaryDirectory() as temp_dir:
        custom_log_dir = Path(temp_dir) / "custom_logs"
        custom_log_dir.mkdir()

        # Configurer avec le répertoire personnalisé
        config = configure_logging(log_directory=str(custom_log_dir))

        logger = get_logger("custom_dir_test")
        logger.info("Test avec répertoire personnalisé")

        print(f"Repertoire configure: {config.log_directory}")
        print(f"Fichiers crees: {list(custom_log_dir.glob('*.log'))}")


def test_user_context():
    """Test avec contexte utilisateur personnalisé."""
    print("\nTest: Contexte utilisateur")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Simuler un utilisateur spécifique
        config = configure_logging(
            log_directory=temp_dir,
            user_id="admin_utilisateur",
            session_id="session_admin_789",
        )

        logger = get_logger("user_context_test")
        logger.info("Test avec contexte utilisateur personnalisé")
        logger.error("Erreur avec contexte utilisateur")

        # Vérifier le contenu des logs
        debug_log = config.debug_log_path
        if debug_log.exists():
            with open(debug_log, encoding="utf-8") as f:
                content = f.read()
                print("Contenu du log avec contexte:")
                print(content)

                if "user=admin_utilisateur" in content:
                    print("Contexte utilisateur correctement injecte")
                if "session=session_admin_789" in content:
                    print("Contexte session correctement injecte")


def test_max_files_limit():
    """Test de la limite de fichiers."""
    print("\nTest: Limite de fichiers")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Configurer avec une limite de 3 fichiers
        config = configure_logging(log_directory=temp_dir, max_log_files=3)

        logger = get_logger("max_files_test")
        logger.info("Test de la limite de fichiers")

        # Vérifier le nombre de fichiers
        log_files = list(Path(temp_dir).glob("*.log"))
        print(f"Fichiers de logs crees: {len(log_files)}")

        if len(log_files) <= 6:  # 3 debug + 3 error max
            print("Limite de fichiers respectee")
        else:
            print("Limite de fichiers non respectee")


def interactive_test():
    """Test interactif pour l'utilisateur."""
    print("\nTest interactif")
    print("=" * 30)

    # Demander à l'utilisateur de définir des variables
    print("Définissez les variables d'environnement suivantes:")
    print("(Laissez vide pour utiliser les valeurs par défaut)")

    log_dir = input("MANG_LOG_DIR (répertoire de logs): ").strip()
    user_id = input("MANG_USER_ID (identifiant utilisateur): ").strip()
    session_id = input("MANG_SESSION_ID (identifiant session): ").strip()
    max_files = input("MANG_LOG_MAX_FILES (limite fichiers): ").strip()

    # Définir les variables si fournies
    if log_dir:
        os.environ["MANG_LOG_DIR"] = log_dir
    if user_id:
        os.environ["MANG_USER_ID"] = user_id
    if session_id:
        os.environ["MANG_SESSION_ID"] = session_id
    if max_files:
        os.environ["MANG_LOG_MAX_FILES"] = max_files

    # Configurer le logging
    config = configure_logging()

    logger = get_logger("interactive_test")
    logger.info("Test interactif avec variables personnalisées")
    logger.warning("Avertissement de test")
    logger.error("Erreur de test")

    print("\nConfiguration finale:")
    print(f"   Repertoire: {config.log_directory}")
    print(f"   Fichier debug: {config.debug_log_path.name}")
    print(f"   Fichier error: {config.error_log_path.name}")
    print(f"   Run ID: {config.run_identifier}")


def main():
    """Fonction principale."""
    print("Test des variables d'environnement pour le logging")
    print("=" * 60)

    try:
        demonstrate_environment_variables()
        test_custom_log_directory()
        test_user_context()
        test_max_files_limit()

        # Demander si l'utilisateur veut faire le test interactif
        response = (
            input("\nVoulez-vous faire le test interactif? (o/n): ").strip().lower()
        )
        if response in ["o", "oui", "y", "yes"]:
            interactive_test()

        print("\nTests termines!")

    except Exception as e:
        print(f"\nErreur: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
