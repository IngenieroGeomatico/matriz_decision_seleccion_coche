import random
import time
from typing import Optional, Sequence

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def generar_user_agent():
    return [
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:112.0) Gecko/20100101 Firefox/112.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36"
    ]

def generar_sleep(TIME_SLEEP_BASE = 1, max=0.5, min=-0.5):
    time.sleep(TIME_SLEEP_BASE + random.uniform(min, max))

def crear_session_robusta(max_retries: int = 10,
                          backoff_factor: float = 2,
                          status_forcelist: Sequence[int] = (429, 500, 502, 503, 504)) -> requests.Session:
    """Crea una `requests.Session` con reintentos y backoff exponencial.

    Usa `urllib3.util.retry.Retry` para manejar reintentos en fallos transitorios.
    """
    session = requests.Session()
    retry = Retry(
        total=max_retries,
        read=max_retries,
        connect=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def robust_get(session: requests.Session, url: str, headers: Optional[dict] = None, params : Optional[dict] = None, timeout: int = 20) -> requests.Response:
    """Realiza una petición GET usando la sesión proporcionada y retorna la respuesta.

    Lanza `requests.RequestException` si la petición falla.
    """
    response = session.get(url, headers=headers, params=params, timeout=timeout)
    response.raise_for_status()
    return response
