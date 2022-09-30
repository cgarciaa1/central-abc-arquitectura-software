import random

# Generamos una clase que lee si el elemento al que le estamos implementando el hash es STORED o es SENT. Si es SENT le agregamos un randomizador para fallar aleatoreamente 1 de cada 5 intentos. Posteriormente agregamos la SALT dependiendo del randomizador para la prueba. Finalmente, determinamos si los HASH (el enviado y el stored) son iguales.


class Signal:
    def __init__(self, signal_event, signal_value, signal_stored):
        self.signal_event = signal_event
        self.signal_value = signal_value
        self.signal_stored = signal_stored

    def __hash__(self):
        randomizer = 1 if self.signal_stored == 'stored' else random.randint(
            1, 5)
        salt = '12345678910' if randomizer == 1 else '01987654321'
        concat_value = str(self.signal_value) + salt
        print('Este ejemplo es ' + ('VALIDO' if randomizer == 1 else 'INVALIDO'))
        return hash((self.signal_event, concat_value))


# Este será el HASH que enviaremos al validador.
sent_signal = Signal('Temperature', 80, 'sent')
print("El HASH del envío es: %d" % hash(sent_signal))

# Este es el HASH que tenemos almacenado.
signal_stored = Signal('Temperature', 80, 'stored')
print("El HASH del almacenado es: %d" % hash(signal_stored))

# Resultado final de comparar ambos HASH
isSame = (hash(signal_stored) == hash(sent_signal))
print("RESULTADO: ", ("El hash es igual" if isSame else "El Hash es Distinto"))
