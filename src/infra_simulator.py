from src.logger import logger
from src.machine import Machine


def main():
    logger.info("Provisioning started.")

    m = Machine(name="web-server", os="Ubuntu", cpu="2vCPU", ram="4GB")
    m.log_creation()
    logger.info(str(m.to_dict()))

    logger.info("Provisioning ended.")


if __name__ == "__main__":
    main()
