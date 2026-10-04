# AppWebI_2-2026 | Tarea de EC2

### Diferencia principal en correr en 120.0.0.1 y 172.31.x.x

    - `127.0.0.1` en tu curl es tu **propia laptop**, no la instancia EC2. Ahí no hay nada corriendo, por eso falla instantáneo.
    - `172.31.22.204` es la **IP privada** de la instancia (rango VPC), solo accesible desde dentro de la misma red de AWS. Desde tu laptop, por internet, esa IP no es enrutable — por eso el segundo curl tarda 132 segundos y luego falla (timeout, no rechazo).

    Necesitas la **IP pública** de la instancia (la que usas para el SSH, ej. algo como `34.230.84.157`). Prueba:

    ```bash
    curl http://<IP_PUBLICA>:5000
    ```

    Si tampoco responde, revisa el **Security Group** de la instancia en la consola de AWS: necesita una regla de entrada (inbound) para TCP puerto 5000 desde tu IP (o 0.0.0.0/0 para pruebas).

https://claude.ai/share/e9be53c3-3a5b-457a-8a12-529316b24950

### Puerto 0.0.0.0

EL puerto 0.0.0.0 es el puerto que se permite escuchar todas las interfaces de red disponibles

https://share.google/aimode/DFPiY9NS1ldJHtWC4