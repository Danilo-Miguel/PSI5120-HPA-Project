import subprocess
import matplotlib.pyplot as plt
import time

# Função para executar o Apache Bench (ab)
def run_ab(url, requests, concurrency):
    command = f"ab -n {requests} -c {concurrency} {url}"
    print(f"Executando comando: {command}")  # Para depuração
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Verificando se houve erro na execução do comando
    if result.returncode != 0:
        print(f"Erro ao executar o comando: {result.stderr}")
        return ""
    
    return result.stdout

# Função para contar o número de pods em execução
def count_running_pods():
    command = "kubectl get pods -l app=nginx --field-selector=status.phase=Running --no-headers | wc -l"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return int(result.stdout.strip())

# Função para obter a utilização da CPU
def get_cpu_usage():
    command = "kubectl top pods -l app=nginx --no-headers | awk '{sum += $3} END {print sum}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return float(result.stdout.strip().replace('%', ''))

# URL do serviço com NodePort no Minikube
url = "http://192.168.49.2:32704/"

# Armazenar requisições por segundo, número de pods e porcentagem de CPU
request_rates = []
pod_counts = []
cpu_usages = []

# Rodar 5 testes
for i in range(5):
    print(f"Executando teste {i+1}")
    output = run_ab(url, 50000, 100)
    
    # Capturar e armazenar a taxa de requisições por segundo
    for line in output.splitlines():
        if "Requests per second:" in line:
            request_rate = float(line.split(":")[1].strip().split()[0])
            request_rates.append(request_rate)

    # Capturar e armazenar o número de pods em execução
    pod_count = count_running_pods()
    pod_counts.append(pod_count)

    # Capturar e armazenar a porcentagem de uso da CPU
    cpu_usage = get_cpu_usage()
    cpu_usages.append(cpu_usage)

    # Aguardar 10 segundos antes do próximo teste
    time.sleep(1)

# Criar gráfico para taxa de requisições
plt.figure(figsize=(10, 5))
plt.plot(request_rates, label='Requisições por Segundo', color='blue', marker='o')
plt.title('Taxa de Requisições por Segundo em Testes de Carga')
plt.xlabel('Número do Teste')
plt.ylabel('Requisições por Segundo')
plt.xticks(range(len(request_rates)))
plt.legend()
plt.grid()
plt.savefig('resultado_requisicoes.png')

# Criar gráfico para contagem de pods
plt.figure(figsize=(10, 5))
plt.plot(pod_counts, label='Número de Pods em Execução', color='green', marker='o')
plt.title('Contagem de Pods em Execução em Testes de Carga')
plt.xlabel('Número do Teste')
plt.ylabel('Número de Pods')
plt.xticks(range(len(pod_counts)))
plt.legend()
plt.grid()
plt.savefig('resultado_pods.png')

# Criar gráfico: Requisições por Segundo e Uso de CPU
plt.figure(figsize=(10, 5))
plt.plot(request_rates, label='Requisições por Segundo', color='blue', marker='o')
plt.title('Requisições por Segundo e Uso de CPU')
plt.xlabel('Número do Teste')
plt.ylabel('Requisições por Segundo')
plt.xticks(range(len(request_rates)))
plt.legend(loc='upper left')
plt.grid()

# Eixo secundário para a porcentagem de uso da CPU
ax = plt.gca()  # Obtém o eixo atual
ax2 = ax.twinx()  
ax2.plot(cpu_usages, color='red', marker='x', label='Uso da CPU (%)')
ax2.set_ylabel('Porcentagem de CPU (%)', color='red')
ax2.tick_params(axis='y', labelcolor='red')
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('resultado_requisicoes_cpu.png')

# Criar gráfico horizontal: Número de Pods e Uso de CPU
fig, ax3 = plt.subplots(figsize=(10, 5))
ax3.plot(pod_counts, label='Número de Pods em Execução', color='green', marker='o')
ax3.set_title('Número de Pods em Execução e Uso de CPU')
ax3.set_xlabel('Número do Teste')
ax3.set_ylabel('Número de Pods')
ax3.tick_params(axis='y', labelcolor='green')

# Eixo secundário para a porcentagem de uso da CPU
ax4 = ax3.twinx()  
ax4.set_ylabel('Porcentagem de CPU (%)', color='red')
ax4.plot(cpu_usages, color='red', marker='x', label='Uso da CPU (%)')
ax4.tick_params(axis='y', labelcolor='red')

plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig('resultado_pods_cpu_horizontal.png')

print("Teste concluído.")
