# PSI5120-HPA-Project

## Nginx Kubernetes Deployment with horizontal Auto-Scaling

This project demonstrates the deployment of an Nginx web server on a Kubernetes cluster using Minikube with automatic horizontal scaling.

## Prerequisites

- Ubuntu on WSL
- Docker
- Kubectl
- Minikube

## Installation Steps

### 1. Instalar e configurar o docker

- Atualizar a lista de pacotes
sudo apt update

- Instalar pacotes necessários </br>
`sudo apt install apt-transport-https ca-certificates curl software-properties-common`

- Adicionar a chave GPG oficial do Docker </br>
`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`

- Adicionar repositório Docker </br>
`echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
`
- Atualizar a lista de pacotes novamente </br>
`sudo apt update
`
- Instalar o Docker </br>
`sudo apt install docker-ce docker-ce-cli containerd.io
`
- Verificar a instalação do Docker </br>
`sudo docker --version
`
- Adicione seu usuário ao grupo docker </br>
`sudo usermod -aG docker $USER
`
- Aplique as mudanças do grupo </br>
`newgrp docker
`

### 2. Instalar o Kubectl

- Baixar o binário do kubectl </br>
`curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
`
- Tornar o binário executável </br>
`chmod +x kubectl
`
- Mover o binário para o PATH </br>
`sudo mv kubectl /usr/local/bin/
`
- Verificar a instalação do kubectl </br>
`kubectl version --client
`
### 3. Instalar o Minikube

- Baixar o binário do Minikube </br>
`curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
`
- Tornar o binário executável </br>
`chmod +x minikube-linux-amd64
`
- Mover o binário para o PATH </br>
`sudo mv minikube-linux-amd64 /usr/local/bin/minikube
`
- Verificar a instalação do Minikube </br>
`minikube version
`
### 4. Inicializar Minikube 

- Iniciar Minikube com o driver Docker </br>
`minikube start --driver=docker
`
- Verificar o status do cluster Minikube </br>
`minikube status
`
### 5. Aplicar e expor o Deplyoment como serviço 

- Aplicar o Deployment </br>
`kubectl apply -f nginx-deployment.yaml
`
- Expor o Deployment como um serviço </br>
`kubectl expose deployment nginx-deployment --type=NodePort --port=80
`
- Obter a URL do Serviço exposto. Uma observação sobre essa etapa:  Essa etapa irá manter o serviço em execução, portanto, o terminal no qual o comando for executado ficará bloqueado, então é necessário executar as etapas seguintes em outro terminal ou executar o comando em background. </br>
`minikube service nginx-deployment --url
`
### 6. Configurar o Autoescalamento Horizontal Automático

-  Habilitar o Metrics Server </br>
`minikube addons enable metrics-server
`
- Aplicar o Autoescalador Horizontal </br>
`kubectl apply -f nginx-hpa.yaml
`
### 7. Teste de carga. Foram executados testes com 3 ferramentas diferentes.

Testes com o Apache Benchmark  </br>
- Instalar o Apache Benchmark </br>
`sudo apt install apache2-utils
`
- Executando o teste com Apache BenchMark. Explicando o comando abaixo: "ab" faz referência ao ferramenta, "-n" especifica o total de requisições, "-c", concorrência e URL faz referência a URL do serviço. </br>
`ab -n 1000 -c 10 http://127.0.0.1:PORT/
`
Teste com o Siege </br>
- Instalar o Siege </br>
`sudo apt install siege
`
- Executando teste com o Siege. Explicando o comando abaixo: "siege" faz referência a ferramenta, "-c" concorrência, "-t" duração do teste e URL faz referência a URL do serviço exposto. </br>
`-c 10 -t 1m http://127.0.0.1:PORT/
` 
