import subprocess

def ejecutar_comando():
    try:
        # Ejecutar el script json_to_text.py
        comando_json = subprocess.run(["python", r"indexacion\json_to_txt.py"], check=True)
        
        # Ejecutar el script Map.py y pasar la salida como entrada al script Reduce.py
        comando_map = subprocess.Popen(["python", r"indexacion\map.py"], stdout=subprocess.PIPE)
        
        comando_reduce = subprocess.Popen(["python", r"indexacion\reduce.py"], stdin=comando_map.stdout, stdout=subprocess.PIPE)
        comando_map.stdout.close()  # Permitir que comando_map reciba una señal SIGPIPE si comando_reduce finaliza.
        
        salida = comando_reduce.communicate()[0]
        print("Proceso map|reduce completado con éxito.")
    except subprocess.CalledProcessError as e:
        if e.output is not None:
            print("Mensaje de error:", e.output.decode('utf-8'))
        else:
            print("Mensaje de error: No hay salida disponible.")

if __name__ == "__main__":
    ejecutar_comando()

