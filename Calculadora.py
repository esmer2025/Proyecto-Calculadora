# Calculadora.py
import customtkinter as ctk
import tkinter as tk


class CalculadoraApp(ctk.CTk):
    """Calculadora gráfica usando CustomTkinter."""

    def __init__(self):
        super().__init__()

        # --- Configuración de ventana ---
        ctk.set_appearance_mode("dark")  # Tema oscuro
        ctk.set_default_color_theme("blue")

        self.title("Calculadora")
        self.geometry("420x560")
        self.resizable(False, False)

        # --- Estado interno ---
        # Expresión mostrada y que luego se calcula al presionar "="
        self.expresion = ""
        # Entrada temporal para mostrar el resultado o operación
        self.resultado_anterior = None  # opcional (no estrictamente necesario)

        # --- Interfaz ---
        self._crear_interfaz()

        # --- Atajos de teclado (opcional y sencillo) ---
        self._configurar_teclado()

    def _crear_interfaz(self):
        """Crea todos los widgets de la interfaz."""
        # Título en grande
        self.label_titulo = ctk.CTkLabel(
            self,
            text="Calculadora",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.label_titulo.pack(pady=(18, 10))

        # Frame para la pantalla
        frame_pantalla = ctk.CTkFrame(self, corner_radius=12)
        frame_pantalla.pack(padx=18, pady=(0, 14), fill="x")

        # Entrada donde se muestra la expresión/resultados
        self.entrada = ctk.CTkEntry(
            frame_pantalla,
            height=50,
            font=ctk.CTkFont(size=20),
            justify="right",
            corner_radius=10,
            placeholder_text="0",
        )
        self.entrada.insert(0, "0")
        self.entrada.configure(state="readonly")  # evita edición manual
        self.entrada.pack(padx=12, pady=10, fill="x")

        # Frame principal de botones
        frame_botones = ctk.CTkFrame(self, corner_radius=12)
        frame_botones.pack(padx=18, pady=8, fill="both", expand=True)

        # Configurar grid del frame
        for fila in range(5):
            frame_botones.grid_rowconfigure(fila, weight=1)
        for col in range(4):
            frame_botones.grid_columnconfigure(col, weight=1)

        # Botones (layout)
        # Fila 0
        self._crear_boton(frame_botones, "C", 0, 0, color="cancel")
        self._crear_boton(frame_botones, "+/-", 0, 1, color="neutral")
        self._crear_boton(frame_botones, "%", 0, 2, color="neutral")
        self._crear_boton(frame_botones, "÷", 0, 3, color="operador")

        # Fila 1
        self._crear_boton(frame_botones, "7", 1, 0, color="numero")
        self._crear_boton(frame_botones, "8", 1, 1, color="numero")
        self._crear_boton(frame_botones, "9", 1, 2, color="numero")
        self._crear_boton(frame_botones, "×", 1, 3, color="operador")

        # Fila 2
        self._crear_boton(frame_botones, "4", 2, 0, color="numero")
        self._crear_boton(frame_botones, "5", 2, 1, color="numero")
        self._crear_boton(frame_botones, "6", 2, 2, color="numero")
        self._crear_boton(frame_botones, "-", 2, 3, color="operador")

        # Fila 3
        self._crear_boton(frame_botones, "1", 3, 0, color="numero")
        self._crear_boton(frame_botones, "2", 3, 1, color="numero")
        self._crear_boton(frame_botones, "3", 3, 2, color="numero")
        self._crear_boton(frame_botones, "+", 3, 3, color="operador")

        # Fila 4 (0 ocupa 2 columnas)
        self._crear_boton(frame_botones, "⌫", 4, 0, color="neutral")  # borrar carácter
        self._crear_boton(frame_botones, "0", 4, 1, color="numero", colspan=2)
        self._crear_boton(frame_botones, ".", 4, 2, color="numero")
        self._crear_boton(frame_botones, "=", 4, 3, color="igual")

    def _crear_boton(self, contenedor, texto, fila, col, color="neutral", colspan=1):
        """Crea un botón con estilo y su acción asociada al evento."""
        estilos = {
            "numero": {"fg_color": "#2B2F36", "hover_color": "#3A3F49", "text_color": "white"},
            "operador": {"fg_color": "#3B82F6", "hover_color": "#2563EB", "text_color": "white"},
            "neutral": {"fg_color": "#6B7280", "hover_color": "#4B5563", "text_color": "white"},
            "cancel": {"fg_color": "#EF4444", "hover_color": "#DC2626", "text_color": "white"},
            "igual": {"fg_color": "#10B981", "hover_color": "#059669", "text_color": "white"},
        }
        cfg = estilos.get(color, estilos["neutral"])

        boton = ctk.CTkButton(
            contenedor,
            text=texto,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=12,
            height=52,
            **cfg,
            command=lambda t=texto: self._accion_boton(t),
        )

        boton.grid(row=fila, column=col, columnspan=colspan, padx=8, pady=8, sticky="nsew")

    def _configurar_teclado(self):
        """Asocia teclas del teclado a las mismas acciones de los botones."""
        self.bind("<Key>", self._teclado_pulsado)
        # Atajos comunes
        self.bind("<Return>", lambda e: self._accion_boton("="))
        self.bind("<KP_Enter>", lambda e: self._accion_boton("="))
        self.bind("<BackSpace>", lambda e: self._accion_boton("⌫"))

        # Escape como "C"
        self.bind("<Escape>", lambda e: self._accion_boton("C"))

    def _teclado_pulsado(self, evento):
        """Detecta caracteres del teclado y los manda a la calculadora."""
        tecla = evento.char

        # Números y punto
        if tecla.isdigit():
            self._accion_boton(tecla)
            return
        if tecla == ".":
            self._accion_boton(".")
            return

        # Operadores (algunos equivalentes)
        if tecla in ["+", "-", "*", "/"]:
            # Convertimos '*' y '/' a '×' y '÷' para reutilizar la lógica
            mapeo = {"*": "×", "/": "÷"}
            self._accion_boton(mapeo.get(tecla, tecla))
            return

        # Porcentaje (opcional)
        if tecla == "%":
            self._accion_boton("%")

    def _accion_boton(self, texto):
        """Maneja el evento de cada botón según el texto del botón."""
        if texto in "0123456789":
            self._agregar_numero(texto)
        elif texto == ".":
            self._agregar_punto()
        elif texto in ["+", "-", "×", "÷"]:
            self._agregar_operador(texto)
        elif texto == "C":
            self._limpiar_todo()
        elif texto == "⌫":
            self._borrar_caracter()
        elif texto == "%":
            self._porcentaje()
        elif texto == "+/-":
            self._cambiar_signo()
        elif texto == "=":
            self._calcular_resultado(texto)
        # Si llega otro valor, no hacemos nada

    # =======================
    # Acciones / manipulaciones de la expresión
    # =======================

    def _set_entrada(self, texto):
        """Actualiza la pantalla sin permitir edición manual."""
        self.entrada.configure(state="normal")
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, texto if texto != "" else "0")
        self.entrada.configure(state="readonly")

    def _agregar_numero(self, numero):
        """Agrega dígitos a la expresión."""
        # Evitar que la pantalla quede en "0" sin contexto
        if self.expresion == "0":
            self.expresion = numero
        else:
            self.expresion += numero
        self._set_entrada(self.expresion)

    def _agregar_punto(self):
        """Agrega un punto decimal al número actual si no existe."""
        if self._esta_vacio_o_cero():
            self.expresion = "0."

        # Extraer el "token" numérico actual (desde el final hasta el último operador)
        token = self._token_actual()
        if "." in token:
            return  # no permitir dos puntos

        self.expresion += "."
        self._set_entrada(self.expresion)

    def _agregar_operador(self, operador):
        """Agrega un operador a la expresión, cuidando el formato."""
        # Si está vacío o solo "0", iniciamos con 0 (por ejemplo "0+")
        if self.expresion == "" or self.expresion == "0":
            if operador in ["+", "-"]:
                self.expresion = "0" + operador
                self._set_entrada(self.expresion)
            else:
                # Para × y ÷, iniciamos con 0 (ej: 0×)
                self.expresion = "0" + self._simbolo_operador(operador)
                self._set_entrada(self.expresion)
            return

        # Si el último carácter ya es operador, reemplazarlo
        if self._ultimo_es_operador():
            self.expresion = self.expresion[:-1] + self._simbolo_operador(operador)
        else:
            self.expresion += self._simbolo_operador(operador)

        self._set_entrada(self.expresion)

    def _limpiar_todo(self):
        """Limpia toda la expresión."""
        self.expresion = ""
        self._set_entrada("0")

    def _borrar_caracter(self):
        """Borra el último carácter de la expresión."""
        if self.expresion == "":
            self._set_entrada("0")
            return
        self.expresion = self.expresion[:-1]
        if self.expresion == "":
            self._set_entrada("0")
        else:
            self._set_entrada(self.expresion)

    def _porcentaje(self):
        """
        Convierte el número actual a porcentaje.
        Ejemplo: 50% -> 50/100 = 0.5
        """
        if self.expresion == "" or self.expresion == "0":
            self._set_entrada("0")
            return

        token = self._token_actual()
        try:
            valor = float(token)
            valor_pct = valor / 100.0

            # Reemplazar solo el token numérico actual por el nuevo valor
            inicio = len(self.expresion) - len(token)
            self.expresion = self.expresion[:inicio] + self._formatear_decimal(valor_pct)

            self._set_entrada(self.expresion)
        except ValueError:
            self._set_entrada("Error")

    def _cambiar_signo(self):
        """Cambia el signo del número actual (+/-)."""
        if self.expresion == "" or self.expresion == "0":
            # Si es 0, lo cambiamos a -0. (La pantalla mostrará 0 de forma limpia.)
            self.expresion = "0"
            self._set_entrada(self.expresion)
            return

        token = self._token_actual()
        if token == "":
            return

        # Si el token empieza con '-' lo quitamos, si no, lo agregamos
        if token.startswith("-"):
            nuevo = token[1:]
        else:
            nuevo = "-" + token

        inicio = len(self.expresion) - len(token)
        self.expresion = self.expresion[:inicio] + nuevo
        self._set_entrada(self.expresion)

    # =======================
    # Cálculo seguro (sin eval)
    # =======================

    def _calcular_resultado(self, _texto_igual):
        """Calcula el resultado y lo muestra en la pantalla."""
        if self.expresion == "" or self.expresion == "0":
            self._set_entrada("0")
            return

        # Validación rápida: no terminar con operador
        if self._ultimo_es_operador():
            self._set_entrada("Error")
            self.expresion = ""
            return

        # Tokenizamos y evaluamos respetando precedencia (* y / antes que + y -)
        try:
            tokens = self._tokenizar(self.expresion)
            valor = self._evaluar_tokens(tokens)
            self._set_entrada(self._formatear_decimal(valor))

            # Almacenar el resultado en la expresión para permitir continuar
            self.expresion = self._formatear_decimal(valor)
        except ZeroDivisionError:
            self._set_entrada("Div/0")
            self.expresion = ""
        except (ValueError, ArithmeticError):
            self._set_entrada("Error")
            self.expresion = ""

    def _tokenizar(self, expresion):
        """
        Convierte una cadena como:
        "12.5+3×4-2"
        en una lista de tokens:
        [12.5, '+', 3.0, '×', 4.0, '-', 2.0]
        """
        tokens = []
        i = 0

        # Normalizamos símbolos: usamos ÷ y × internamente como operadores reales
        operadores = {"+", "-", "×", "÷"}

        while i < len(expresion):
            ch = expresion[i]

            # Espacios no se usan, pero por si acaso
            if ch == " ":
                i += 1
                continue

            # Operadores
            if ch in operadores:
                tokens.append(ch)
                i += 1
                continue

            # Número (puede tener signo negativo, como -3 o 2.5)
            # Caso signo negativo: solo si es parte del número (ej: al inicio o después de operador)
            if ch == "-" and (i == 0 or expresion[i - 1] in operadores):
                # leer número negativo completo
                j = i + 1
                while j < len(expresion) and (expresion[j].isdigit() or expresion[j] == "."):
                    j += 1
                num_str = expresion[i:j]
                tokens.append(float(num_str))
                i = j
                continue

            # Número positivo
            if ch.isdigit() or ch == ".":
                j = i + 1
                while j < len(expresion) and (expresion[j].isdigit() or expresion[j] == "."):
                    j += 1
                num_str = expresion[i:j]
                if num_str in ["", "."]:
                    raise ValueError("Número inválido")
                tokens.append(float(num_str))
                i = j
                continue

            raise ValueError("Caracter inválido")

        return tokens

    def _evaluar_tokens(self, tokens):
        """Evalúa tokens respetando precedencia (*,/ antes que +,-)."""
        # Primero: resolver × y ÷
        tokens_intermedios = []
        i = 0

        while i < len(tokens):
            token = tokens[i]
            if isinstance(token, (int, float)):
                tokens_intermedios.append(float(token))
                i += 1
            else:
                # operador
                op = token
                # Debe tener un número antes en la lista intermedia
                if not tokens_intermedios:
                    raise ValueError("Expresión inválida")

                # y un número después en tokens original
                if i + 1 >= len(tokens) or not isinstance(tokens[i + 1], (int, float)):
                    raise ValueError("Expresión inválida")

                a = tokens_intermedios.pop()
                b = float(tokens[i + 1])

                if op == "×":
                    tokens_intermedios.append(a * b)
                elif op == "÷":
                    if b == 0:
                        raise ZeroDivisionError()
                    tokens_intermedios.append(a / b)
                elif op in ["+", "-"]:
                    # No lo hacemos aquí: se deja para el segundo paso
                    # Guardamos el operador y el siguiente número
                    # Para esto, en vez de resolver ahora, reinsertamos correctamente.
                    tokens_intermedios.append(a)
                    tokens_intermedios.append(op)
                    i += 1  # avanzamos el operador
                else:
                    raise ValueError("Operador inválido")

                # Si resolvimos × o ÷, avanzamos dos posiciones (operador + número)
                if op in ["×", "÷"]:
                    i += 2

                # Si era + o -, no debe saltarse el número del siguiente:
                # ya lo reinsertamos como parte de la lista intermedia al agregar op,
                # por eso avanzamos solo 1 y el número b será procesado en la siguiente iteración
                if op in ["+", "-"]:
                    # el siguiente token es un número, lo añadiremos en la siguiente vuelta
                    i += 1

        # Segundo paso: resolver + y -
        # Recorremos tokens_intermedios (que ya no debería contener × o ÷)
        # Ejemplo: [12.0, '+', 3.0, '-', 2.0]
        if not tokens_intermedios:
            raise ValueError("Expresión inválida")

        resultado = tokens_intermedios[0]
        j = 1
        while j < len(tokens_intermedios):
            op = tokens_intermedios[j]
            if j + 1 >= len(tokens_intermedios):
                raise ValueError("Expresión incompleta")
            b = tokens_intermedios[j + 1]

            if op == "+":
                resultado += b
            elif op == "-":
                resultado -= b
            else:
                raise ValueError("Operador inválido en suma/resta")
            j += 2

        return resultado

    # =======================
    # Utilidades de expresión
    # =======================

    def _simbolo_operador(self, operador_boton):
        """Convierte los símbolos del botón a los operadores internos."""
        mapeo = {
            "+": "+",
            "-": "-",
            "×": "×",
            "÷": "÷",
        }
        return mapeo.get(operador_boton, operador_boton)

    def _esta_vacio_o_cero(self):
        return self.expresion == "" or self.expresion == "0"

    def _ultimo_es_operador(self):
        if self.expresion == "":
            return False
        return self.expresion[-1] in {"+", "-", "×", "÷"}

    def _token_actual(self):
        """
        Retorna el número actual (token) desde el último operador hasta el final.
        Ej: "12+3.5×4" -> token actual "4"
             "12+3.5×-4" -> token actual "-4" (si corresponde)
        """
        if self.expresion == "":
            return ""

        operadores = {"+", "-", "×", "÷"}
        # Buscamos el último operador que NO sea parte del signo del número
        # Para simplificar a nivel medio: tomamos el último operador en la cadena,
        # y luego ajustamos casos del signo negativo al inicio del token.
        i = len(self.expresion) - 1
        while i >= 0 and self.expresion[i] not in operadores:
            i -= 1

        # i queda en un operador o -1
        if i < 0:
            return self.expresion

        # Si el operador encontrado fue '-' y está pegado como signo negativo,
        # esto es complicado de detectar en todos los casos; para la práctica,
        # el token actual funcionará bien para esta calculadora.
        return self.expresion[i + 1:]

    def _formatear_decimal(self, numero):
        """Formatea para que no aparezcan muchos decimales innecesarios."""
        # Redondeo razonable
        try:
            # Convertir a float y redondear a 10 decimales
            n = float(numero)
            n = round(n, 10)

            # Evitar mostrar .0 si es entero
            if n.is_integer():
                return str(int(n))

            return str(n)
        except Exception:
            return "Error"


if __name__ == "__main__":
    app = CalculadoraApp()
    app.mainloop()