import json
import time

def retrieve_phone_code(driver) -> str:
    """
    Función para interceptar y obtener el código de confirmación del teléfono
    desde las solicitudes de red registradas por Chrome.
    """
    for _ in range(10):
        time.sleep(1)
        logs = driver.get_log("performance")
        for entry in logs:
            try:
                message = json.loads(entry["message"])["message"]
                if message["method"] == "Network.responseReceived":
                    url = message["params"]["response"]["url"]
                    if "api/v1/number?number=" in url:
                        request_id = message["params"]["requestId"]
                        response = driver.execute_cdp_cmd(
                            "Network.getResponseBody", {"requestId": request_id}
                        )
                        body = json.loads(response["body"])
                        if isinstance(body, dict) and "code" in body:
                            return str(body["code"])
            except Exception:
                pass
    raise Exception("No se encontró el código de confirmación en los registros de rendimiento.")