from module.NeuroPy import NeuroPy
import time
import os
from tqdm import tqdm

object1 = NeuroPy("/dev/tty.usbmodem4971314A36591", 115200, '7d55')

volume = [50, 50, 50, 50, 50]

# Inizializza la barra di avanzamento per il volume
volume_bar = tqdm(total=100, desc="Volume", position=0, leave=True)

def attention_callback(value):
    # Regola il volume in base al valore di attenzione
    os.system(f"osascript -e 'set volume output volume {value}'")

def meditation_callback(value):
    # Aggiorna la lista del volume e calcola la media
    volume.append(value)
    volume.pop(0)
    avg_value = sum(volume) / len(volume)

    # Regola il volume in base alla media dei valori di meditazione
    os.system(f"osascript -e 'set volume output volume {avg_value}'")

    # Aggiorna la barra di avanzamento del volume
    volume_bar.update(avg_value - volume_bar.n)



# Imposta i callback
object1.setCallBack("attention", attention_callback)
object1.setCallBack("meditation", meditation_callback)

# Avvia 
object1.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Programma interrotto dall'utente.")
except Exception as e:
    print(f"Errore durante l'esecuzione del programma: {e}")
finally:
    # Chiudi la barra di avanzamento
    volume_bar.close()

    print("Chiusura del programma.")
    object1.stop()

