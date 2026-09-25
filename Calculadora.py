# Calculadora.py
import customtkinter as ctk
import tkinter as tk
import re
from decimal import Decimal, localcontext


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
        self.resultado_anterior = None
        self.resultado_mostrado = False

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

        # Fila 4: un botón por columna, sin superposición
        self._crear_boton(frame_botones, "⌫", 4, 0, color="neutral")  # borrar carácter
        self._crear_boton(frame_botones, "0", 4, 1, color="numero")
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
        if tecla in (".", ","):
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
        if len(texto) == 1 and texto in "0123456789":
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
        """Inicia otra cuenta tras =, o agrega un dígito al número actual."""
        if self.resultado_mostrado:
            self.expresion = ""
            self.resultado_mostrado = False
        token = self._token_actual()
        if token in ("0", "-0"):
            self.expresion = self.expresion[:-1] + numero
        else:
            self.expresion += numero
        self._set_entrada(self.expresion)

    def _agregar_punto(self):
        """Añade un único punto decimal y actualiza siempre la pantalla."""
        if self.resultado_mostrado:
            self.expresion = ""
            self.resultado_mostrado = False
        token = self._token_actual()
        if "." in token:
            return
        self.expresion += "0." if not token else "."
        self._set_entrada(self.expresion)

    def _agregar_operador(self, operador):
        """Agrega un operador a la expresión, cuidando el formato."""
        self.resultado_mostrado = False
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
        self.resultado_mostrado = False
        self.resultado_anterior = None
        self._set_entrada("0")

    def _borrar_caracter(self):
        """Borra el último carácter de la expresión."""
        self.resultado_mostrado = False
        if self.expresion == "":
            self._set_entrada("0")
            return
        self.expresion = self.expresion[:-1]
        if self.expresion == "":
            self._set_entrada("0")
        else:
            self._set_entrada(self.expresion)

    def _porcentaje(self):
        """Convierte solo el número actual: 50% = 0.5 (divide entre 100)."""
        token = self._token_actual()
        if not token:
            return
        with localcontext() as contexto:
            contexto.prec = max(28, len(token) + 10)
            valor = Decimal(token) / Decimal(100)
        inicio = len(self.expresion) - len(token)
        self.expresion = self.expresion[:inicio] + self._formatear_decimal(valor)
        self._set_entrada(self.expresion)

    def _cambiar_signo(self):
        """Alterna el signo del último número sin cambiar la operación."""
        token = self._token_actual()
        if not token:
            # Permite introducir un negativo al inicio o después de un operador.
            self.expresion += "-0"
        else:
            nuevo = token[1:] if token.startswith("-") else "-" + token
            inicio = len(self.expresion) - len(token)
            self.expresion = self.expresion[:inicio] + nuevo
        self._set_entrada(self.expresion)

    def _calcular_resultado(self, _texto_igual="="):
        """Calcula con prioridad de multiplicación y división, sin usar eval."""
        try:
            tokens = self._tokenizar(self.expresion or "0")
            valor = self._evaluar_tokens(tokens)
            self.expresion = self._formatear_decimal(valor)
            self.resultado_anterior = valor
            self.resultado_mostrado = True
            self._set_entrada(self.expresion)
        except ZeroDivisionError:
            self._limpiar_todo()
            self._set_entrada("Div/0")
        except (ValueError, ArithmeticError):
            self._limpiar_todo()
            self._set_entrada("Error")

    def _tokenizar(self, expresion):
        """Distingue la resta del signo negativo: 5--3 equivale a 5 - (-3)."""
        tokens = []
        i = 0
        espera_numero = True
        while i < len(expresion):
            if expresion[i].isspace():
                i += 1
                continue
            if espera_numero:
                coincidencia = re.match(r"-?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)", expresion[i:])
                if coincidencia is None:
                    raise ValueError("Se esperaba un número")
                tokens.append(Decimal(coincidencia.group()))
                i += len(coincidencia.group())
            else:
                if expresion[i] not in "+-×÷":
                    raise ValueError("Se esperaba un operador")
                tokens.append(expresion[i])
                i += 1
            espera_numero = not espera_numero
        if not tokens or espera_numero:
            raise ValueError("Expresión incompleta")
        return tokens

    def _evaluar_tokens(self, tokens):
        """Resuelve × y ÷ primero; después + y - de izquierda a derecha."""
        if not tokens or len(tokens) % 2 == 0:
            raise ValueError("Expresión inválida")
        for i, token in enumerate(tokens):
            if i % 2 == 0:
                if not isinstance(token, Decimal) or not token.is_finite():
                    raise ValueError("Número inválido")
            elif token not in ("+", "-", "×", "÷"):
                raise ValueError("Operador inválido")

        with localcontext() as contexto:
            # Precisión suficiente para conservar los dígitos introducidos.
            contexto.prec = max(28, sum(len(str(t)) for t in tokens) + 10)
            terminos = [tokens[0]]
            for i in range(1, len(tokens), 2):
                operador, numero = tokens[i], tokens[i + 1]
                if operador == "×":
                    terminos[-1] *= numero
                elif operador == "÷":
                    if numero == 0:
                        raise ZeroDivisionError()
                    terminos[-1] /= numero
                else:
                    # Conservamos AMBOS: operador y número siguiente.
                    terminos.extend([operador, numero])

            resultado = terminos[0]
            for i in range(1, len(terminos), 2):
                if terminos[i] == "+":
                    resultado += terminos[i + 1]
                else:
                    resultado -= terminos[i + 1]
            return resultado

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
        """Obtiene el último número, incluyendo su signo si es negativo."""
        i = len(self.expresion)
        while i > 0 and self.expresion[i - 1] in "0123456789.":
            i -= 1
        if i == len(self.expresion):
            return ""
        if (i > 0 and self.expresion[i - 1] == "-"
                and (i == 1 or self.expresion[i - 2] in "+-×÷")):
            i -= 1
        return self.expresion[i:]

    def _formatear_decimal(self, numero):
        """Evita notación científica, ceros finales y errores de tipo float."""
        if not numero.is_finite():
            raise ValueError("Resultado no finito")
        if numero == 0:
            return "0"
        texto = format(numero, "f")
        return texto.rstrip("0").rstrip(".") if "." in texto else texto


if __name__ == "__main__":
    app = CalculadoraApp()
    app.mainloop()