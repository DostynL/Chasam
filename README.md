Discussion Questions


1. Hash function design
Si solo hasheáramos una frecuencia, muchas canciones tendrían los mismos hashes y el sistema no podría distinguirlas. Al usar el triplete (f1, f2, Δt) cada huella es mucho más única porque combina dos frecuencias y el tiempo entre ellas. Si quitas un componente las colisiones se disparan y el reconocimiento falla.

2. Collision analysis
El load factor se mantiene bajo 0.75 porque la tabla hace resize automático. La cadena más larga es corta y el promedio está cerca de 1, lo que confirma que el lookup es O(1) en la práctica.

3. Capacity & primes
Con capacidad primo el módulo usa todos los bits del hash y las claves se distribuyen parejo. Con potencia de 2 solo se usan los bits bajos y hay más colisiones entre claves similares.

4. Resizing cost
El resize es O(n) porque hay que reinsertar todo. Pero como la capacidad se duplica cada vez, no pasa seguido y el costo amortizado por inserción sigue siendo O(1).

5. Fan-out trade-off
FAN_OUT=5 es más rápido y ocupa menos memoria pero reconoce peor en condiciones con ruido. FAN_OUT=30 reconoce mejor pero es más lento y ocupa más. FAN_OUT=15 es el punto medio que funciona bien para ambos casos.

6. Robustness
Funciona con ruido y volumen diferente porque usa bandas de frecuencia en vez de bins exactos y un umbral por percentil en vez de amplitud fija. No importa desde qué parte suena la canción porque la coherencia temporal solo necesita que los offsets sean consistentes, no que empiecen desde el mismo punto.

7. Time coherence
Si solo contamos matches directos, una canción con muchas huellas comunes ganaría aunque no sea la correcta. El histograma soluciona esto porque solo la canción correcta va a tener un pico claro donde todos los deltas coinciden. Las demás tendrán deltas dispersos sin ningún pico.
