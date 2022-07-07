"""In acest modul este configurata aplicatia."""
import uvicorn

try:
    import uvloop
except ModuleNotFoundError:
    print("[*] Running without `uvloop`")
    uvloop = ...
from app.configuration import incarcare_configuratie
from app.program import configurare_aplicatie
from app.services import configurare_services

if uvloop is not ...:
    uvloop.install()

app = configurare_aplicatie(*configurare_services(incarcare_configuratie()))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
