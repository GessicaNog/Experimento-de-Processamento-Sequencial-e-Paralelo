import time
from concurrent.futures import ProcessPoolExecutor


def tarefa(numero):
    resultado = 0

    for i in range(1, 300_000):
        resultado += (numero * i) % 97

    return resultado


def tarefa_balanceada(numero):
    if numero % 10 == 0:
        limite = 1_500_000
    else:
        limite = 300_000

    resultado = 0

    for i in range(1, limite):
        resultado += (numero * i) % 97

    return resultado


def executar_sequencial(dados, funcao=tarefa):
    inicio = time.perf_counter()

    resultados = []

    for numero in dados:
        resultados.append(funcao(numero))

    fim = time.perf_counter()

    return resultados, fim - inicio


def executar_paralelo(dados, workers, funcao=tarefa):
    inicio = time.perf_counter()

    with ProcessPoolExecutor(max_workers=workers) as executor:
        resultados = list(executor.map(funcao, dados))

    fim = time.perf_counter()

    return resultados, fim - inicio


def experimento(dados, nome):
    print("\n" + "=" * 60)
    print(nome)
    print("=" * 60)

    _, tempo_sequencial = executar_sequencial(dados)

    print(f"Tempo sequencial: {tempo_sequencial:.6f} segundos")

    print("\nProcessos | Tempo (s) | Speedup | Eficiência")

    # Resultado do sequencial
    print(
        f"{1:^9} | "
        f"{tempo_sequencial:^10.6f} | "
        f"{1.0:^7.2f} | "
        f"{1.0:^10.2%}"
    )

    for workers in [2, 4, 8]:

        _, tempo_paralelo = executar_paralelo(dados, workers)

        speedup = tempo_sequencial / tempo_paralelo
        eficiencia = speedup / workers

        print(
            f"{workers:^9} | "
            f"{tempo_paralelo:^10.6f} | "
            f"{speedup:^7.2f} | "
            f"{eficiencia:^10.2%}"
        )


def experimento_balanceamento(dados):
    print("\n" + "=" * 60)
    print("EXPERIMENTO DE BALANCEAMENTO DE CARGA")
    print("=" * 60)

    _, tempo_sequencial = executar_sequencial(
        dados,
        tarefa_balanceada
    )

    print(f"Tempo sequencial: {tempo_sequencial:.6f} segundos")

    print("\nProcessos | Tempo (s) | Speedup | Eficiência")

    print(
        f"{1:^9} | "
        f"{tempo_sequencial:^10.6f} | "
        f"{1.0:^7.2f} | "
        f"{1.0:^10.2%}"
    )

    for workers in [2, 4, 8]:

        _, tempo_paralelo = executar_paralelo(
            dados,
            workers,
            tarefa_balanceada
        )

        speedup = tempo_sequencial / tempo_paralelo
        eficiencia = speedup / workers

        print(
            f"{workers:^9} | "
            f"{tempo_paralelo:^10.6f} | "
            f"{speedup:^7.2f} | "
            f"{eficiencia:^10.2%}"
        )


if __name__ == "__main__":

    # ETAPA 1 e 2
    dados = list(range(1, 101))

    experimento(
        dados,
        "EXPERIMENTO PRINCIPAL - 100 TAREFAS"
    )

    # ETAPA 5 - GRANULARIDADE
    experimento(
        list(range(1, 21)),
        "EXPERIMENTO A - 20 TAREFAS"
    )

    experimento(
        list(range(1, 101)),
        "EXPERIMENTO B - 100 TAREFAS"
    )

    experimento(
        list(range(1, 501)),
        "EXPERIMENTO C - 500 TAREFAS"
    )

    # ETAPA 6 - BALANCEAMENTO
    experimento_balanceamento(
        list(range(1, 101))
    )