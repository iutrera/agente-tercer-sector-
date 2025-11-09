"""
Programador de tareas semanales
Ejecuta la actualización de eventos todos los lunes
"""
import schedule
import time
import logging
from datetime import datetime
from weekly_updater import WeeklyUpdater

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('siria_scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run_weekly_task():
    """Ejecuta la tarea semanal de actualización"""
    logger.info("=" * 80)
    logger.info(f"SCHEDULED TASK TRIGGERED - {datetime.now().isoformat()}")
    logger.info("=" * 80)

    try:
        updater = WeeklyUpdater()
        results = updater.run_full_update()

        # Enviar email con resultados
        if results.get('status') == 'success':
            updater.send_weekly_email(results)
            logger.info("Weekly update completed successfully")
        else:
            logger.error("Weekly update failed")
            logger.error(f"Errors: {results.get('errors', [])}")

    except Exception as e:
        logger.error(f"Error in scheduled task: {e}", exc_info=True)


def main():
    """
    Programa la ejecución semanal todos los lunes a las 09:00
    """
    logger.info("SIRIA Scheduler started")
    logger.info("Scheduling weekly updates for every Monday at 09:00")

    # Programar tarea para todos los lunes a las 09:00
    schedule.every().monday.at("09:00").do(run_weekly_task)

    # También permitir ejecución manual inmediata (comentar en producción)
    # schedule.every(1).minutes.do(run_weekly_task)

    logger.info("Scheduler is running. Press Ctrl+C to stop.")

    # Loop infinito
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto

        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in scheduler loop: {e}")
            time.sleep(60)


if __name__ == '__main__':
    main()
